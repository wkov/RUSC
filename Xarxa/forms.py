__author__ = 'z'
from django import forms
from .models import Aportacio, Debat, Resum, Vote, Votedebat, Link
from .models import UserProfile
import autocomplete_light
from tagging.models import Tag

autocomplete_light.autodiscover()
autocomplete_light.register(Tag)

#ModelForm
class AportacioForm(forms.ModelForm):
    # titol = forms.CharField
    # entradilla = forms.TextInput
    # tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
    #                                       widget=TagSelectMultiple(attrs={ 'style': 'width:300px' }))
    class Meta:
        model = Aportacio
        exclude = {"autor","datahora","rank_score","debat_id", "links", "video", "country", "tema", "seccio"}
        # widgets = {
        # 	'tags': TagSelectMultiple(attrs={ 'style': 'width:300px' }),
       	# }
        widgets = {
        	'tags': autocomplete_light.TextWidget('TagAutocomplete'),
            # 'text': forms.Textarea(attrs={'onChange': 'get_links()'} )
       	}

class DebatForm(forms.ModelForm):
    class Meta:
        model = Debat
        exclude = {"autor","debat","parent","aportacio","datahora", "rank_score"}

class ResumForm(forms.ModelForm):
    class Meta:
        model = Resum

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = {"user"}



class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote

class VotedebForm(forms.ModelForm):
    class Meta:
        model = Votedebat

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link


from registration.forms import RegistrationForm
from django.forms import ModelForm
from models import UserProfile

#descomentar la seguent linea per a que apareixin tots els camps en el registre
RegistrationForm.base_fields.update(UserProfileForm.base_fields)

#per a que el registre grabi realment tots els camps s han de ficar tots dins el seguent Form i en l'arxiu regbackend.py
#analitzar be el seguent forum per a decidir si cambiem aixo: http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django
#el que esta fet es basa en: http://stackoverflow.com/questions/14726725/python-django-django-registration-add-an-extra-field

#en la meva opinio son massa camps com per un registre, massa LENT

class UserRegForm(RegistrationForm):
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=30)
    birthday = forms.DateField()
    job = forms.CharField(max_length=30)
    # activity = forms.CharField(max_length=30)
    # city = forms.CharField(max_length=30)
    # country = forms.CharField(max_length=20)
    # bio = forms.Textarea()
    # situacion_laboral = forms.CharField(max_length=20)
    # web = forms.CharField(max_length=30)