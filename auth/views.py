from django.shortcuts import render_to_response as render, redirect
from oauth import oauth
from utils import *
from django.contrib.auth.models import User
from models import UserProfile
from django.template.context import RequestContext as rc
import re
from django.contrib.auth.decorators import login_required
from tools import facebook

def validate(email):
	errors = []
	if email and not re.compile( \
		'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$').match( \
		email):
		errors += ['email']
	return errors

def index(req):
    if req.user.is_authenticated():
        return redirect('/home/')
    login_facebook_url = 'https://graph.facebook.com/oauth/authorize?client_id=%s&redirect_uri=%s&scope=publish_stream,email' % (settings.APP_ID_FACEBOOK, settings.URL+'/login/facebook/')
    args = {
        'login_facebook_url':login_facebook_url
    }
    return render('index.html', args, context_instance = rc(req))

def about(req):
    args = {}
    return render('about.html', args, context_instance = rc(req))

@login_required
def info(req):
    if req.user.is_authenticated():
        if len(req.user.email) is not 0:
            return redirect('/home/')
	if req.POST:
		req.user.email = req.POST['email']
		errors = validate(req.POST['email'])
		if not errors:
		    req.user.save()
		    return redirect('/home/')
		return render('info.html', {
			'user': req.user,
			'errors': errors
		})
	return render('info.html', {'user': req.user}, rc(req))

def login_with_facebook(req):
    url = 'https://graph.facebook.com/oauth/access_token?client_id='+settings.APP_ID_FACEBOOK+'&redirect_uri='+settings.URL+'/login/facebook/&client_secret='+settings.SECRET_KEY_FACEBOOK+'&code='+req.GET['code']
    token = str(urllib2.urlopen(url).read()).split('=')[1]
    fb = facebook.GraphAPI(token)
    data = fb.get_object('me')
    user = None
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email']
        )
        profile = UserProfile.objects.create(
            facebook_token=token,
            user=user,
            image = 'https://graph.facebook.com/'+data['username']+'/picture'
        )
    except:
        user = User.objects.get(username=data['username'])
    from django.contrib.auth import login, load_backend
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
    if hasattr(user, 'backend'):
        login(req, user)
    return redirect('/home/')

def login_with_twitter(req):
    token = get_unauthorized_token()
    req.session['token'] = token.to_string()
    return redirect(get_authorization_url(token))

def callback(req):
    token = req.session.get('token', None)
    if not token:
        return render('callback.html', {
            'token': True
        })
    token = oauth.OAuthToken.from_string(token)
    if token.key != req.GET.get('oauth_token', 'no-token'):
        return render('callback.html', {
            'mismatch': True
        })
    token = get_authorized_token(token)
    obj = is_authorized(token)
    if obj is None:
        return render('callback.html', {
            'username': True
        })
    user = None
    try:
        user = User.objects.get(username=obj['screen_name'])
    except:
        user = User(username=obj['screen_name'])
    user.save()
    profile = None
    try:
        profile = user.get_profile()
    except:
        profile = UserProfile(user=user)
    profile.oauth_token = token.key
    profile.oauth_token_secret = token.secret
    profile.followers = obj['followers_count']
    profile.image = obj['profile_image_url']
    try:
        profile.location = obj['location']
    except:
        pass
    try:
        profile.lang = obj['lang']
    except:
        pass
    try:
        profile.time_zone = obj['time_zone']
    except:
        pass
    profile.save()
    from django.contrib.auth import login, load_backend
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
    if hasattr(user, 'backend'):
        login(req, user)
    del req.session['token']
    return redirect('/info/')

@login_required
def logout(req):
    from django.contrib.auth import logout
    logout(req)
    return redirect('/')

@login_required
def home(req):
    args = {}
    return render('home.html', args, context_instance=rc(req))
