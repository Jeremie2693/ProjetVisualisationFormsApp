from django import forms
#from listings.models import Csv

'''
class CsvModelForm(forms.ModelForm):
    class Meta:
        model = Csv 
        fields = {'file_name',}

'''
from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField
