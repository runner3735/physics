
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Course, Demo, Room

class NameForm(forms.Form):
  name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'size': '128'}))

class TagForm(forms.Form):
  text = forms.CharField(max_length=128, label='', widget=forms.TextInput(attrs={'size': '80'}))
  
class CourseForm(forms.Form):
  course = forms.ModelMultipleChoiceField(queryset=Course.objects.all(), widget=forms.CheckboxSelectMultiple, label='')
  
class RoomForm(forms.Form):
  room = forms.ModelChoiceField(queryset=Room.objects.all(), required=False, empty_label='Unknown', widget=forms.RadioSelect, label='')

class LocationForm(forms.Form):
  location = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '128'}))
  help_text="(Enter location of demo within room)"

  def clean_location(self):
    data = self.cleaned_data['location']
    if "Gorilla" in data:
      raise ValidationError(_('Invalid location - Gorilla cannot be in location'))
    return data

class NewPhotoForm(forms.Form):
  imagefile = forms.ImageField()
  caption = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '128'}))

class UpdatePhotoForm(forms.Form):
  imagefile = forms.ImageField(required=False, label='Replace With')
  caption = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '128'}))
  
class NoteForm(forms.Form):
  text = forms.CharField(max_length=2048, label="", widget=forms.Textarea(attrs={'cols': '100', 'rows': '5'}))
  
class DescriptionForm(forms.Form):
  description = forms.CharField(max_length=2048, required=False, label="", widget=forms.Textarea(attrs={'cols': '100', 'rows': '20'}))
  
class NewFileForm(forms.Form):
  otherfile = forms.FileField()
  description = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '103'}))

class UpdateFileForm(forms.Form):
  otherfile = forms.FileField(required=False, label='Replace With')
  description = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'size': '103'}))
  
class DemoForm(forms.ModelForm):
  class Meta:
    model = Demo
    fields = '__all__'
    widgets = {'name': forms.TextInput(attrs={'size': '103'}),
               'description': forms.Textarea(attrs={'cols': '100'}),
               'location': forms.TextInput(attrs={'size': '103'}),
               'course': forms.CheckboxSelectMultiple(),
               'room': forms.RadioSelect()
               }
  def __init__(self, *args, **kwargs):
    super(DemoForm, self).__init__(*args, **kwargs)
    self.fields['room'].empty_label = 'Unknown' 
