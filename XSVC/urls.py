from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required as auth
# import autocomplete_light
# # import every app/autocomplete_light_registry.py
# autocomplete_light.autodiscover()
from Xarxa.views import AportacioxTagListView, LinkFormView
from Xarxa.views import DebatListView, EscritoriListView, ResumListView, AportacioListView, AportacioCreateView, VoteFormView, AportacioxTemaListView
from Xarxa.views import AportacioDetailView, UserProfileDetailView, UserProfileEditView, AportacioUpdateView, VotedebatFormView, ResumxTemaListView
from Xarxa.views import DebatCreateView, DebatDetailView, DebatUpdateView, ResumCreateView, ResumDetailView, ResumUpdateView, UserProfileDeleteView
# Uncomment the next two lines to enable the admin:
import notification
from notification import urls
from Xarxa.forms import UserRegForm
import regbackend
from registration.backends.default.views import RegistrationView
import postman
import micawber




from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'XSVC.views.home', name='home'),
    # url(r'^XSVC/', include('XSVC.foo.urls')),
    url(r'^$', EscritoriListView.as_view() ,name='escritori'),
    url(r'^aportacions/(?P<pk>\d+)/debats/$', DebatListView.as_view() ,name="debats"),
    url(r"^login/$", "django.contrib.auth.views.login",
        {"template_name": "login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login",
        name="logout"),
    url(r'^aportacions/$', AportacioListView.as_view() ,name='aportacions'),
    url(r'^aportacions/create/$', AportacioCreateView.as_view() ,name='aportacio_create'),
    url(r"^aportacions/update/(?P<pk>\d+)/$", auth(AportacioUpdateView.as_view()),
        name="aportacio_update"),
    url(r"^aportacions/(?P<pk>\d+)/$", AportacioDetailView.as_view(),
        name="aportacio_detail"),
    url(r'^aportacions/(?P<pk>\d+)/debats/reply/(?P<id>\d+)/$', DebatCreateView.as_view() ,name='debat_create'),
    # url(r'^aportacions/(?P<pk>\d+)/debats/reply/$', FirstDebatCreateView.as_view() ,name='first_debat_create'),
    url(r"^debat/update/(?P<pk>\d+)/$", auth(DebatUpdateView.as_view()),
        name="debat_update"),
    url(r"^debat/(?P<pk>\d+)/$", DebatDetailView.as_view(),
        name="debat_detail"),
    url(r'^resums/$', ResumListView.as_view() ,name='resums'),
    url(r'^resum/create/$', ResumCreateView.as_view() ,name='resum_create'),
    url(r"^resum/update/(?P<pk>\d+)/$", auth(ResumUpdateView.as_view()),
        name="resum_update"),
    url(r"^resum/(?P<pk>\d+)/$", ResumDetailView.as_view(),
        name="resum_detail"),
    url('^inbox/notifications/', include(notification.urls)),
    url(r'^tema/(?P<pk>\d+)/aportacions/$', AportacioxTemaListView.as_view() ,name='aportacionsxtema'),
    url(r'^tema/(?P<pk>\d+)/resums/$', ResumxTemaListView.as_view() ,name='resumsxtema'),
    url(r'^tag/(?P<slug>\w+)/aportacions/$', AportacioxTagListView.as_view() ,name='aportacionsxtag'),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    (r'^messages/', include('postman.urls')),
    # url(r'^note/', include('notification.urls')),
    url(r'^votedebat/$', auth(VotedebatFormView.as_view()), name="votedebat"),
    url(r'^charts/(?P<pk>\d+)/simple.png$', 'Xarxa.views.pygraphviz_graph', name="chart"),
    # url(r'^resums/$', 'Xarxa.views.resums' ,name='resums'),
    # url(r'^aportacions/$', 'Xarxa.views.aportacions' ,name='aportacions'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r"^accounts/", include("registration.backends.simple.urls")),
    url(r"^users/delete/(?P<slug>\w+)/$", auth(UserProfileDeleteView.as_view()), name="registration_delete"),
    url(r'^accounts/register/$', RegistrationView.as_view(),
        {'backend': 'registration.backends.default.DefaultBackend','form_class': UserRegForm}, name='registration_register'),
    url(r"^accounts/", include('registration.backends.default.urls')),
    url(r"^users/(?P<slug>\w+)/$", UserProfileDetailView.as_view(),
        name="profile"),
    url(r"edit_profile/$", auth(UserProfileEditView.as_view()),
        name="edit_profile"),
    url(r'^link/$', LinkFormView.as_view(), name="link"),
    url(r'^url/$', 'Xarxa.views.link_verify'),
    url(r'^vote/$', auth(VoteFormView.as_view()), name="vote"),
#les seguents 4 url's s'utilitzen per a recuperar la conta quan has olvidat la contrasenya
#basat en: http://garmoncheg.blogspot.com.au/2012/07/django-resetting-passwords-with.html
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    (r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect' : '/user/password/done/'}),
    (r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),
)
