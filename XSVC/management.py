__author__ = 'sergi'
from django.conf import settings
from django.db.models import signals
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("comment_to_app", _("Nou comentari"), _("Nou comentari a la teva aportacio"))
        notification.create_notice_type("comment_to_com", _("Nou comentari"), _("Nou comentari en un fil on participes"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"


