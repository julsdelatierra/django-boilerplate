from django.conf import settings
from django.shortcuts import render_to_response as render, redirect
from django.template.context import RequestContext as rc

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
