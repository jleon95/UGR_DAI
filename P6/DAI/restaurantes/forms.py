# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

class register_form(forms.ModelForm):
    username = forms.SlugField(max_length=8,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Username:')
    first_name = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='First name')
    last_name = forms.CharField(max_length=40,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Last name')
    password = forms.SlugField(max_length=8,\
           widget=forms.PasswordInput(attrs={'class': 'form-control'}),\
           label='Password:')
    class Meta:
        model  = User
        fields = ('username', 'first_name', 'last_name', 'password')

class update_form(forms.ModelForm):
    first_name = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='First name')
    last_name = forms.CharField(max_length=40,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Last name')
    class Meta:
        model  = User
        fields = ('first_name', 'last_name')

class login_form(forms.ModelForm):
    username = forms.SlugField(max_length=8,\
                    widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2'}),\
                    label='Username:')
    password = forms.SlugField(max_length=8,\
           widget=forms.PasswordInput(attrs={'class': 'form-control mr-sm-2'}),\
           label='Password:')
    class Meta:
        model  = User
        fields = ('username', 'password')
