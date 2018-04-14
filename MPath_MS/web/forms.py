from django import forms
from .models import SBMLfile

class SBMLFileForm(forms.ModelForm):
    class Meta:
        model = SBMLfile
        fields = ['file']