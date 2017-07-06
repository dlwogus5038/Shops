from django.shortcuts import render

# Create your views here.
from .models import Shop, Comment
from .models import User, Request_Friend
#from .models import Friend
from .forms import SearchForm
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
import json
import jieba
import gensim
# from pre_process.generate_index_file_defs import get_stop_words


dictionary_file = 'pre_process/comment_dictionary.dict'
lsi_file = 'pre_process/comment_lsi.lsi'
index_file = 'pre_process/comment_index.index'
shop_ids_file = 'pre_process/comment_ids.txt'
# comment_file = 'pre_process/comments.txt'
# stop_words_file = 'pre_process/stop_words.txt'
ranking_list_num = 3
max_ranking_list_size = 20


def home(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_choice = search_form.cleaned_data['search_choice']
            sort_choice = search_form.cleaned_data['sort_choice']
            search_input = search_form.cleaned_data["search_input"]
            if search_choice == 'LOC' or search_choice == 'FOODTYPE':  # search by property
                return render(request, 'home/home.html', {'search_form': search_form, 'search_choice': search_choice, 'char_input': search_input,
                                                          'shops': search_by_property(search_choice, sort_choice, search_input)})
            elif search_choice == 'COMMENT':  # search by content
                comments = search_by_comment(search_input)
                return render(request, 'home/home.html', {'search_form': search_form, 'comments': comments})
            return render(request, 'home/home.html', {'search_form': search_form})
    search_form = SearchForm()
    return render(request, 'home/home.html', {'search_form': search_form})


def userprofile(request, username):
    profile_user = User.objects.get(username=username)
    user = request.user
    try:
        friend = user.friend.get(username = profile_user)
    except ObjectDoesNotExist:
        friend = user
    try:
        profile_friends = profile_user.friend.all()
    except ObjectDoesNotExist:
        profile_friends = profile_user

    try:
        request_freinds = profile_user.request_friend_set.all()
    except ObjectDoesNotExist:
        request_freinds = profile_user

    return render(request, 'home/userprofile.html' ,
                  {'profile_user' : profile_user,'friend' : friend,'profile_friends' : profile_friends
                      ,'request_freinds' : request_freinds })


def search_by_property(search_choice, sort_choice, char_input):
    shops = []  # show shop information
    if search_choice == 'LOC':
        shops = Shop.objects.filter(loc=char_input).order_by('-' + sort_choice.lower())
    elif search_choice == 'FOODTYPE':
        shops = Shop.objects.filter(foodtype=char_input).order_by('-' + sort_choice.lower())
    return shops[:50]


def show_statistics(request, search_choice, char_input):
    shops = []
    order_by = 'foodtype'
    if search_choice == 'LOC':
        shops = Shop.objects.filter(loc=char_input)
    elif search_choice == 'FOODTYPE':
        shops = Shop.objects.filter(foodtype=char_input)
        order_by = 'loc'
    shops_distinct = shops.values(order_by).distinct()
    shops = shops.values()
    statistics = {}  # a dict recording shop number for each foodtype
    statistics_json = []
    for i, distinct_shop in enumerate(shops_distinct):
        name = distinct_shop[order_by]
        statistics[name] = 0
        for shop in shops:
            if shop[order_by] == name:
                statistics[name] += 1
        statistics_json.append({'value': statistics[name], 'name': name})
    return render(request, 'home/statistics.html', {'statistics': json.dumps(statistics_json)})


def search_by_comment(search_input):
    # pre-procession
    words = jieba.cut(search_input)
    # stop_words_list = get_stop_words(stop_words_file)
    # words = [word for word in words if not word in stop_words_list]
    dictionary = gensim.corpora.Dictionary.load(dictionary_file)
    lsi = gensim.models.LsiModel.load(lsi_file)
    query_lsi = lsi[dictionary.doc2bow(words)]

    index = gensim.similarities.Similarity.load(index_file)
    sims = index[query_lsi]
    max_shop_num = 20
    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:max_shop_num]

    comment_ids = []
    with open(shop_ids_file) as f:
       lines = f.readlines()
       comment_ids = [int(lines[item[0]]) for item in sims]
    comments = Comment.objects.filter(pk__in=comment_ids)
    return comments


def show_ranking_lists(request):
    order_by = 'taste'
    shops = Shop.objects.all().order_by('-' + order_by)
    ranking_lists = {}

    # ranking lists of typical food, e.g. 最好吃的面馆
    food = '面'
    ranking_list = shops.filter(shopname__contains=food)
    ranking_lists[food] = ranking_list
    food = '肉'
    ranking_list = shops.filter(shopname__contains=food)
    ranking_lists[food] = ranking_list

    # ranking lists of typical types, e.g. 西餐排行榜
    # calculate shop num of categories, and show the following type of shops:
    categories_count = Shop.objects.count_occurrence(classify_by='foodtype')[:ranking_list_num]
    for category in categories_count:
        # ranking_list = []
        # for shop in shops:
        #     if shop[classify_by] == category[0]:
        #         shop = {'分类': shop[classify_by], '店名': shop['shopname'], '评分': shop[order_by]}
        #         ranking_list.append(shop)
        # ranking_lists[category[0]] = ranking_list[:max_ranking_list_size]
        ranking_lists[category[0]] = shops.filter(foodtype=category[0])
    return render(request, 'home/ranking_lists.html', {'ranking_lists': ranking_lists})


def makefriend(request, username):
    profile_user = User.objects.get(username=username)
    request.user.friend.add(profile_user)
    request.user.save()

    keyset = request.user.request_friend_set.filter(from_user = profile_user).delete()
    request.user.save()
    #profile_user.request_friend.remove(request.user)
    #profile_user.save()
    return render(request, 'home/makefriend.html')

def requestfriend(request, username):
    profile_user = User.objects.get(username=username)
    user = request.user

    request_friend = Request_Friend()
    request_friend.to_user = profile_user
    request_friend.from_user = user.username
    request_friend.save()
    #profile_user.request_friend.add(user)
    #profile_user.save()
    '''
    try:
        friend = user.friend.get(username = profile_user)
    except ObjectDoesNotExist:
        friend = user
    try:
        profile_friends = profile_user.friend.all()
    except ObjectDoesNotExist:
        profile_friends = profile_user
    try:
        request_freinds = profile_user.request_friend.all()
    except ObjectDoesNotExist:
        request_freinds = profile_user
    '''
    return render(request, 'home/requestfriend.html')








