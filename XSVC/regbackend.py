# __author__ = 'sergi'
from Xarxa.models import UserProfile
from Xarxa.forms import UserRegForm
from django.db.models import DateField
from django.db import models
import datetime


def user_created(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    data = UserProfile(user=user)
    data.name = form.data["name"]
    data.surname = form.data["surname"]
    # birthday = DateField()
    # birthday = datetime.datetime.strptime(form.data["birthday"], '%m/%d/%Y').strftime('%Y-%m-%d')
    # data.birthday = birthday
    data.birthday = datetime.datetime.strptime(form.data["birthday"], '%m/%d/%Y').strftime('%Y-%m-%d')
    data.job = form.data["job"]
    # data.activity = form.data["activity"]
    # data.city = form.data["city"]
    # data.country = form.data["country"]
    # data.bio = form.data["bio"]
    # data.situacion_laboral = form.data["situacion_laboral"]
    # data.web = form.data["web"]
    data.save()

from registration.signals import user_registered
user_registered.connect(user_created)