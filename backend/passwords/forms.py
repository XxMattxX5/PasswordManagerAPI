from django import forms

class CreateFolderForm(forms.Form):
    folderName = forms.CharField(max_length=200, required=True)



class CreatePasswordForm(forms.Form):
    accountName = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
    
