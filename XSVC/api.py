from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from Xarxa.models import Aportacio

class AportacioResource(ModelResource):
    class Meta:
        queryset = Aportacio.objects.all()
        resource_name = 'aportacions'
        authorization = Authorization()
        allowed_methods = ['get', 'post', 'delete', 'put']
        always_return_data = True
