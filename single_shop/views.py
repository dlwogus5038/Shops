from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Shop, Comment
from django import forms
import json


def single_shop(request, urlID):
    return render(request, 'single_shop/single_shop.html', {'shop': get_shop_by_id(urlID)})

    #if request.method == 'POST':
    #    pass
    #return HttpResponse("Hello, world. You're at the polls index.")


def get_shop_by_id(urlID):
    shop = Shop.objects.get(urlID=urlID)
    return shop



