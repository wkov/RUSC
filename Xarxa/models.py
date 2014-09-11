from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from datetime import datetime
from django.utils.timezone import now
from django.db.models import Count
import notification
from notification import models as notification
from notification.models import send
from notification.models import *
from tagging.fields import TagField
from django_countries.fields import CountryField
from embed_video.fields import EmbedVideoField
from micawber.parsers import extract
from micawber.contrib.mcdjango.providers import bootstrap_basic
# Create your models here.

class Escritori(models.Model):
    titol = models.CharField(max_length="40")

    def __unicode__(self):
        return "%s" % (self.titol)


class Tema(models.Model):
    name = models.CharField(max_length=15)

    def __unicode__(self):
        return "%s" % (self.name)

class Seccio(models.Model):
    name = models.CharField(max_length=15)
    tema = models.ForeignKey('Tema', related_name='seccions')

    def __unicode__(self):
        return "%s" % (self.name)


class DebatVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(DebatVoteCountManager, self).get_query_set().annotate(votes=Count('votedebats')
        )

class Debat(models.Model):
    titol = models.CharField(max_length="60")
    datahora = models.DateTimeField(default=now,blank=True)
    parent = models.ForeignKey('self', related_name='children', blank=True, null= True)
    autor = models.ForeignKey(User)
    text = models.TextField(max_length=500)
    aportacio = models.ForeignKey('Aportacio', related_name='debats')
    rank_score = models.FloatField(default=0.0)

    with_votes = DebatVoteCountManager()
    objects = models.Manager()


    def __unicode__(self):
        return "%s" % (self.titol)

    def get_absolute_url(self):
        return reverse('debats', kwargs={'pk': self.aportacio_id} )


    def as_tree(self):
        children = list(self.children.all())
        branch = bool(children)
        yield branch, self
        for child in children:
            for next in child.as_tree():
                yield next
        yield branch, None

    def set_rank(self):
        # Based on HN ranking algo at http://amix.dk/blog/post/19574
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2

        delta = now() - self.datahora
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()

#mira el exemple de stealrumors. planteja d'utilitzar django-celery per a refrescar amb frequencia
class LinkVoteCountManager(models.Manager):
    def get_query_set(self):
        return super(LinkVoteCountManager, self).get_query_set().annotate(votes=Count('vote')
        ).order_by('-rank_score', '-votes')

class Link(models.Model):
    url = models.TextField(blank=True, null=True)
    aportacio = models.ForeignKey('Aportacio', related_name='links', null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.url, self.aportacio)

class Aportacio(models.Model):
    titol = models.CharField(max_length="40")
    autor = models.ForeignKey(User)
    datahora = models.DateTimeField(default=now,blank=True, null=True)
    entradilla = models.TextField(max_length="120", blank=True, null=True)
    text = models.TextField()
    rank_score = models.FloatField(default=0.0)
    debat_id = models.CharField(max_length="50", null=True, blank=True)
    tema = models.ForeignKey('Tema', related_name='aportacions', null=True, blank=True)
    seccio = models.ForeignKey('Seccio', related_name='aportacions', null=True, blank=True)
    tags = TagField()
    country = CountryField(null=True, blank=True)
    video = EmbedVideoField(null=True, blank=True)
    # debat = Xarxa.models.Debat()

    with_votes = LinkVoteCountManager()
    objects = models.Manager()


    def __unicode__(self):
        return "%s" % (self.titol)

    def get_absolute_url(self):
        return reverse('aportacions')

    def set_rank(self):
        # Based on HN ranking algo at http://amix.dk/blog/post/19574
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2

        delta = now() - self.datahora
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()



class Resum(models.Model):
    titol = models.CharField(max_length="40")

    def __unicode__(self):
        return "%s" % (self.titol)

    def get_absolute_url(self):
        return reverse('resums')







class Vote(models.Model):
    voter = models.ForeignKey(User)
    aportacio = models.ForeignKey(Aportacio)

    def __unicode__(self):
        return "%s voted %s" % (self.voter.username, self.aportacio.titol)


class Votedebat(models.Model):
    voter = models.ForeignKey(User)
    debat = models.ForeignKey(Debat, related_name="votedebats")

    def __unicode__(self):
        return "%s voted %s" % (self.voter.username, self.debat.titol)

from django.contrib.auth.models import AbstractUser

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    #basic attributes
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    birthday = models.DateField()
    job = models.CharField(max_length=30)
    # activity = models.CharField(max_length=30)
    # city = models.CharField(max_length=30)
    # country = models.CharField(max_length=20)
    # bio = models.TextField(null=True)
    # situacion_laboral = models.CharField(max_length=20)
    # web = models.CharField(max_length=30)
    # Extra attributes
    # foto = models.ImageField(null=True, blank=True, upload_to='/static/img')
    # empresa = models.CharField(max_length=25, null=True, blank=True)
    # cargo = models.CharField(max_length=25)
    # telephone = models.IntegerField(max_length=15)
    # public = models.BooleanField()
    # receive_all_alerts = models.BooleanField()



    def __unicode__(self):
        return "%s's profile" % self.user

# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         profile, created = UserProfile.objects.get_or_create(user=instance)

def deb_ap_create(sender, instance, created, **kwargs):
    if created:
        debat, created = Debat.objects.get_or_create(titol = instance.titol, autor = instance.autor,
                                 datahora = instance.datahora, aportacio = instance)
        instance.debat_id = debat.id

#inici del codi per a llistar els enllacos que hi hagi en el text
    p = bootstrap_basic()
    links = extract(instance.text,p)
    lks = Link.objects.filter(aportacio=None).update(aportacio = instance)

    if links[0]:
        for link in links[0]:
                s = Link.objects.get_or_create(url=link, aportacio=instance)


#fi del codi per llistar enllacos

def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        if not instance.aportacio.autor == instance.autor:
            send([instance.aportacio.autor], "comment_to_app", {"debat": instance})

        # notification.send([instance], "comment_to_app")

        debats = Debat.objects.filter(aportacio=instance.aportacio)
        userz = set()
        for item in debats:
            if not item.autor == instance.autor and item.autor not in userz and not item.autor == instance.aportacio.autor:
                userz.add(item.autor)
        # notification.send_now(userz, 'comment_to_com' )
        for user in userz:
            notification.send([user], "comment_to_com", {"debat": instance})






# def send_notification(sender, aportacio, debat, **kwargs):
    # notification.send([aportacio.autor], "comment_to_app", {"debat": debat})

from django.db.models.signals import post_save
# post_save.connect(create_profile, sender=User)
post_save.connect(deb_ap_create, sender=Aportacio) #Crea la instancia debate de cualquier aportacion creada
post_save.connect(send_comment_notification, sender=Debat)


from django_mailbox.signals import message_received
from django.dispatch import receiver

@receiver(message_received)
def message_rec(sender, message, **args):
    print("kghekjwhgekw")
from django.db import models


#si actives les seguentes 5 linees dona error, no hi ha nota solucionada que ho arregli
#tot i aixo hi ha caracteristiques de la app tagging que requereixen aquest registre
# import tagging
#
#
# tagging.register(Aportacio)


#La classe TagSelectMultiple de moment no s'utilitza, pero es com el seleccionador de destinataris del modul de missatges
# de Facebook. En el futur ens pot interesar per el nostre modul de missatges per escollir destinataris

# from django import forms
# from django.forms.util import flatatt
# from django.utils.encoding import force_unicode
# from django.utils.html import escape, conditional_escape
# from django.utils.safestring import mark_safe
#
# class TagSelectMultiple(forms.SelectMultiple):
#     def render(self, name, value, attrs=None, choices=()):
#         if value is None: value = []
#         final_attrs = self.build_attrs(attrs, name=name)
#         self.name = name
#         output = [u'<div class="tagSelector" multiple="multiple"%s>' % flatatt(final_attrs)]
#         options = self.render_options(choices, value)
#         if options:
#             output.append(options)
#         output.append('<input type=text>')
#         output.append('</div>')
#         return mark_safe(u'\n'.join(output))
#
#     def render_option(self, selected_choices, option_value, option_label):
#         if unicode(option_value) in selected_choices:
#             return u'<span class="tag">%s <a>x</a><input name="%s" type="hidden" value="%s"/></span>' % (
#                 conditional_escape(force_unicode(option_label)), escape(self.name), escape(option_value))
#         return ''




admin.site.register(Escritori)
admin.site.register(Debat)
# admin.site.register(Aportacio)
admin.site.register(Resum)
admin.site.register(Tema)


from .forms import AportacioForm

class AportacioInline(admin.TabularInline):
    form = AportacioForm
    model = Aportacio

class AportacioAdmin(admin.ModelAdmin):
    form = AportacioForm
    list_display = ['titol', 'tags']
    inlines = [AportacioInline]

admin.site.register(Aportacio, AportacioAdmin)


#UserProfileInline i UserAdmin serveixen per a afegir camps extra a l'usuari a traves de la classe UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from Xarxa.models import UserProfile
from forms import UserProfileForm
# admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdmin(UserAdmin):
    # form = UserProfileForm
    # list_display = ['job']
    inlines = [UserProfileInline]

admin.site.unregister(User)  # Unregister user to add new inline ProfileInline
admin.site.register(User, UserAdmin)  # Register User with this inline profile

#Fi de l'ampliacio de camps del user en l'admin. Hem hagut de cancelar la funcio que generava el user_profile a
# traves de evento per a que no sen generin varies i doni error. tambe hem creat el arxiu regbackend a l'arrel de la app
#tambe hem canviat el registration_form a forms.py. tambe hem afegit la url customitzada de registration a urls.py