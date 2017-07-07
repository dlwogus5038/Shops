from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Shop, Comment
from django.core.exceptions import ObjectDoesNotExist
from django import forms
import json
#from home.views import search_by_property


def single_shop(request, id):
    shop= get_shop_by_id(id)
    user = request.user
    if user.is_authenticated:
        try:
            user_shop = user.collect_shop.get(id=shop.id)
        except ObjectDoesNotExist:
            user_shop = user
        return render(request, 'single_shop/single_shop.html',
                      {'shop': shop, 'comments': get_comments(id), 'similar_shops': get_similar_shops(shop)
                          , 'user_shop': user_shop})
    else:
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


def makecomment(request, shop_id, text):
    content = text
    shop = Shop.objects.get(id=shop_id)
    user = request.user
    username = user.username


    user_comment = Comment()
    user_comment.shop = shop
    user_comment.user = user
    user_comment.username = username
    user_comment.content = content
    user_comment.save()

    return render(request, 'single_shop/makecomment.html')


