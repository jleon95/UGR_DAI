from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import collection
from .forms import register_form, login_form, update_form, add_restaurant_form, edit_restaurant_form
from random import randint
from pymongo import ReturnDocument
import json
import urllib as url

@login_required
def add_restaurant(request):
    form = add_restaurant_form()
    context = {'message': 'We are adding a restaurant', 'form': form}

    if request.method == 'POST':
        form = add_restaurant_form(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            restaurant_id = str(randint(10000000,99999999))
            result = collection.insert_one(
                {
                    "address": {
                        "street": d['street'],
                        "zipcode": d['zipcode'],
                        "building": d['building'],
                        "coord": [d['longitude'],d['latitude']]
                    },
                    "borough": d['borough'],
                    "cuisine": d['cuisine'],
                    "grades": [],
                    "name": d['name'],
                    "restaurant_id": restaurant_id
                }
            )

    return render(request, 'add_restaurant.html', context)

@login_required
def edit_restaurant(request):
    context = {}
    if request.method == 'POST':
        form = edit_restaurant_form(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            r = collection.find_one_and_update({'name': d['prev_name'], 'restaurant_id': d['r_id']},\
                        {'$set': {'name': d['name'],'address.street': d['street'],\
                        'address.building': d['building'],'borough': d['borough'],\
                        'address.zipcode': d['zipcode'],'cuisine': d['cuisine'],\
                        'address.coord': [d['longitude'],d['latitude']]}},\
                        return_document=ReturnDocument.AFTER)
            data = {'r_id': d['r_id'], 'name': r['name'], 'prev_name': r['name'],\
                    'street': r['address']['street'], 'building': r['address']['building'],\
                    'borough': r['borough'], 'zipcode': r['address']['zipcode'],\
                    'cuisine': r['cuisine'], 'longitude': r['address']['coord'][0],\
                    'latitude': r['address']['coord'][1]}
            form = edit_restaurant_form(data)
            context['longitude'] = data['longitude']
            context['latitude'] = data['latitude']
        else:
            context['longitude'] = form.cleaned_data['longitude']
            context['latitude'] = form.cleaned_data['latitude']
        context['form'] = form
    else:
        name = request.GET.get('name')
        restaurant_id = request.GET.get('id')
        r = collection.find_one({'name': name, 'restaurant_id': restaurant_id})
        data = {'r_id': restaurant_id, 'name': name, 'prev_name': name,\
                'street': r['address']['street'], 'building': r['address']['building'],\
                'borough': r['borough'], 'zipcode': r['address']['zipcode'],\
                'cuisine': r['cuisine'], 'longitude': r['address']['coord'][0],\
                'latitude': r['address']['coord'][1]}
        form = edit_restaurant_form(data)
        context['longitude'] = data['longitude']
        context['latitude'] = data['latitude']
        context['form'] = form
    return render(request, 'edit_restaurant.html', context)

def register(request):
	form = register_form()
	context = {'message': 'We are in Register', 'form': form}
	if request.method == 'POST':
		form = register_form(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()
			context['message'] =  u'Registered as  %s' % (user.username)
		else:
			context['form'] = form

	return render(request, 'register.html', context)

@login_required
def change_info(request):
    form = update_form()
    context = {'message': 'We are modifying your data', 'form': form}
    if request.method == 'POST':
        form = update_form(request.POST,instance=request.user)
        if form.is_valid():
            user = form.save()
            context['message'] =  u'Change data of  %s' % (user.username)
            context['email'] = user.email
        else:
            context['form'] = form

    context['username'] = request.user.get_username()
    context['email'] = request.user.email

    return render(request, 'change_info.html', context)

def login_view(request):
	form = login_form()
	context = {'loginform': form, 'message':'Logging in'}

	if request.method == 'POST':
		form = login_form(request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None and user.is_active:
			login(request, user)
			context['message'] =  u'Logged in as  %s' % username
		else:
			context['message'] =  u'Wrong username or password'

	return render(request, 'index.html', context)

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/restaurantes/')

@login_required
def profile(request):
    user = request.user
    context = {'username': user.get_username(),\
                'email': user.email}
    return render(request, 'profile.html',context)


def index(request):
    context = {}
    return render(request,'index.html',context)

def ai(request):
    context = {}
    return render(request,'ai.html',context)

def restaurant_search(request):
    context = {}
    return render(request,'restaurant_search.html',context)

def restaurant_charts(request):
    context = {}
    return render(request,'restaurant_charts.html',context)

def get_page(request):
    parameters = request.GET
    field = parameters['field']
    keywords = parameters['keywords']
    keywords = url.parse.unquote_plus(keywords)
    number = int(parameters['number'])
    restaurants = list(collection.find({field: keywords},{'address': 1, \
            'cuisine': 1, 'borough': 1, 'name': 1, 'restaurant_id': 1,\
             '_id': 0}))[(number-1)*20:number*20]
    return HttpResponse(json.dumps(restaurants,ensure_ascii=False))

def get_number_of_pages(request):
    parameters = request.GET
    field = parameters['field']
    keywords = parameters['keywords']
    keywords = url.parse.unquote_plus(keywords)
    number = collection.count({field: keywords})
    return HttpResponse(str(number))

def get_cuisine_stats(request):
    pairs = []
    types = sorted(collection.distinct("cuisine"))
    for t in types:
        pairs.append([t,collection.find({"cuisine": t}).count()])
    return HttpResponse(json.dumps(pairs,ensure_ascii=False))
