"""User account management related forms"""
from django import forms
import account.forms

class SignupForm(account.forms.SignupForm):
    """Form for user account sign-up"""
    name = forms.CharField(max_length=60) 
