from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from .models import Shop, Comment
from django.core.exceptions import ObjectDoesNotExist
from django import forms
import json
#from home.views import search_by_property
import jieba
import gensim
from .forms import CommentForm


def single_shop(request, id):
    shop= get_shop_by_id(id)
    user = request.user
    if user.is_authenticated:
        try:
            user_shop = user.collect_shop.get(id=shop.id)
        except ObjectDoesNotExist:
            user_shop = user

        user.last_visit_shop_id = shop.urlID
        user.save()

        if request.method == 'POST':
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                add_comment(user,comment,id)
                #update_index_files(comment)
                return render(request, 'single_shop/single_shop.html',
                              {'shop': shop, 'comments': get_comments(id),
                               'similar_shops': get_similar_shops(shop), 'form': form, 'user_shop': user_shop})

        form = CommentForm()
        return render(request, 'single_shop/single_shop.html',
                      {'shop': shop, 'comments': get_comments(id), 'similar_shops': get_similar_shops(shop)
                          , 'user_shop': user_shop, 'form': form})
    else:
        return render(request, 'single_shop/single_shop.html',
                      {'shop': shop, 'comments': get_comments(id),
                       'similar_shops': get_similar_shops(shop)})

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

def add_comment(user,comment,id):
    """
    by shangming
    this function is called when a user added a comment, we need to update database and index files
    """
    #  TO DO: insert comment to database here
    shop = get_shop_by_id(id)
    username = user.username

    user_comment = Comment()
    user_comment.shop = shop
    user_comment.user = user
    user_comment.username = username
    user_comment.content = comment
    user_comment.save()
    # TO DO: add the comment and comment id into comments.txt and comment_ids.txt

    pass


def update_index_files(doc):
    """
    by shangming
    """
    # pre-procession
    words = jieba.cut(doc)
    # stop_words_list = get_stop_words(stop_words_file)
    # words = [word for word in words if not word in stop_words_list]
    dictionary = gensim.corpora.Dictionary.load(dictionary_file)
    new_corpus = [dictionary.doc2bow(words)]
    lsi = gensim.models.LsiModel.load(lsi_file)
    lsi.add_documents(new_corpus)
    lsi.save(lsi_file)
    # print("saved lsi file")


