from django import forms
from django.forms import ModelForm, Select
from models import *

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
    url = forms.ModelMultipleChoiceField(queryset=WebPage.objects.all(),widget = forms.CheckboxSelectMultiple,required=False)
    new_url = forms.CharField(max_length=100,required=False)
    delay = forms.IntegerField(label='Delay Between Page Scroll (in seconds)',required=False)

class CollectionNameForm(forms.ModelForm):
    class Meta:
        model = Collection
        exclude = ('url','delay')
    name = forms.CharField(max_length=100,required=False,label='',
                            widget=forms.TextInput(attrs={'placeholder': 'New Collection Name'}))


class WebPageForm(forms.ModelForm):
    class Meta:
        model = WebPage
    url = forms.CharField(max_length=200,required=False,label='',
                            widget=forms.TextInput(attrs={'placeholder': 'New Web Address'}))
    