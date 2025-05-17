from django import forms

class CreateFolderForm(forms.Form):
    """
    Form for validating folder creation input.
    """
    folderName = forms.CharField(max_length=255, required=True)



class CreatePasswordForm(forms.Form):
    """
    Form for validating input when creating a new password entry.
    """
    accountName = forms.CharField(max_length=255, required=True)
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(max_length=255, required=True)
    
