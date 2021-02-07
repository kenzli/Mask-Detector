from django import forms 
from .models import *
  
class FaceForm(forms.ModelForm): 
    class Meta: 
        model = Face 
        fields = ['name', 'Upload_Image'] 
