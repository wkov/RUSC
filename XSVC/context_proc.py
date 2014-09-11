__author__ = 'sergi'



def notif_unseen(request):
    from notification.models import Notice
    if hasattr(request, 'user'):
        notif = Notice.objects.unseen_count_for(request.user.id)
        return {'notif' : notif}
    return {}

def temes(request):
    from Xarxa.models import Tema
    temes = Tema.objects.all()
    return {'temes' : temes}

def current_url(request):
    from django.core.urlresolvers import resolve
    current_url = resolve(request.path_info).url_name
    return {'current_url' : current_url}

