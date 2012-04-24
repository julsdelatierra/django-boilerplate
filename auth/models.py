from django.contrib.auth.models import User
from django.db import models
from oauth import oauth
import re, httplib, simplejson
from utils import *

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	oauth_token = models.CharField(max_length=200)
	oauth_token_secret = models.CharField(max_length=200)
	facebook_token = models.CharField(max_length=200)
	image = models.URLField()
