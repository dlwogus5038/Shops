from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Shop, Comment
from django import forms
import json


def single_shop(request, id):
    return render(request, 'single_shop/single_shop.html', {'shop': get_shop_by_id(id)})

    #if request.method == 'POST':
    #    pass
    #return HttpResponse("Hello, world. You're at the polls index.")


def get_shop_by_id(id):
    shop = Shop.objects.get(id=id)
    return shop



