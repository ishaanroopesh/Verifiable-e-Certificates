from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from . import forms
# Create your views here.

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login') #once the sign up finishes and the user is created, the user is sent back to the login page
    template_name = 'accounts/signup.html'
    
