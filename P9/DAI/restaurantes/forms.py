# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from registration.forms import RegistrationForm

def building_validation(number):
    if number < 1 or number > 2000:
        raise ValidationError("%s doesn't seem to be a building number" % number)

def zipcode_validation(number):
    if number < 10000 or number > 99999:
        raise ValidationError("%s doesn't seem to be a zip code" % number)

def longitude_validation(number):
    if number < -180.0 or number > 180.0:
        raise ValidationError("%s doesn't seem to be a longitude" % number)

def latitude_validation(number):
    if number < -90.0 or number > 90.0:
        raise ValidationError("%s doesn't seem to be a latitude" % number)

class register_form(RegistrationForm,forms.ModelForm):
    username = forms.SlugField(max_length=20,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Username:')
    email = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Mail')
    password1 = forms.CharField(max_length=16,\
                widget=forms.PasswordInput(attrs={'class': 'form-control'}),\
                label='Password')
    password2 = forms.CharField(max_length=16,\
           widget=forms.PasswordInput(attrs={'class': 'form-control'}),\
           label='Repeat password:')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1')

class update_form(forms.ModelForm):
    email = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Mail')
    class Meta:
        model  = User
        fields = ('email',)

class login_form(forms.ModelForm):
    username = forms.SlugField(max_length=20,\
                    widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2'}),\
                    label='Username:')
    password = forms.CharField(max_length=16,\
           widget=forms.PasswordInput(attrs={'class': 'form-control mr-sm-2'}),\
           label='Password:')
    class Meta:
        model  = User
        fields = ('username', 'password')

class add_restaurant_form(forms.Form):
    name = forms.SlugField(max_length=60, strip=True,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Name')
    street = forms.CharField(max_length=100,strip=True,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Street')
    building = forms.IntegerField(validators=[building_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Building number')
    borough = forms.CharField(max_length=50,strip=True,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Borough')
    zipcode = forms.IntegerField(validators=[zipcode_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Zip code')
    cuisine = forms.CharField(max_length=30,required=False,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Cuisine')
    longitude = forms.FloatField(validators=[longitude_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Longitude')
    latitude = forms.FloatField(validators=[latitude_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Latitude')

class edit_restaurant_form(forms.Form):
    name = forms.SlugField(max_length=60, strip=True,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Name')
    prev_name = forms.CharField(max_length=60, strip=True,\
                    widget=forms.HiddenInput(attrs={'type': 'hidden'}))
    r_id = forms.CharField(max_length=10, strip=True,\
                    widget=forms.HiddenInput(attrs={'type': 'hidden'}))
    street = forms.CharField(max_length=100,strip=True,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Street')
    building = forms.IntegerField(validators=[building_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Building number')
    borough = forms.CharField(max_length=50,strip=True,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Borough')
    zipcode = forms.IntegerField(validators=[zipcode_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Zip code')
    cuisine = forms.CharField(max_length=30,required=False,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Cuisine')
    longitude = forms.FloatField(validators=[longitude_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Longitude')
    latitude = forms.FloatField(validators=[latitude_validation],\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Latitude')
