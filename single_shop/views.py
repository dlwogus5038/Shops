from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Shop, Comment
from django import forms
import json
#from home.views import search_by_property


def single_shop(request, id):
    shop= get_shop_by_id(id)
    return render(request, 'single_shop/single_shop.html',
                  {'shop': shop, 'comments': get_comments(id), 'similar_shops': get_similar_shops(shop)})

    #if request.method == 'POST':
    #    pass
    #return HttpResponse("Hello, world. You're at the polls index.")


def get_shop_by_id(id):
    shop = Shop.objects.get(id=id)
    return shop


def get_comments(id):
    comments = Comment.objects.filter(shop_id=id)
    return comments


def get_similar_shops(shop):
    similar_shops = Shop.objects.filter(foodtype=shop.foodtype).order_by('-taste')
    result = []
    i = 0
    for s in similar_shops:
        if s.id != shop.id:
            result.append(s)
            i = i + 1
        if i == 5:
            break
    return result


