from django.shortcuts import render

# Create your views here.
from .models import Shop, Comment,ProfileSite
# from .forms import SearchForm
# from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth.models import User
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
    # if request.method == 'POST':
    #     search_form = SearchForm(request.POST)
    #     if search_form.is_valid():
    #         search_choice = search_form.cleaned_data['search_choice']
    #         sort_choice = search_form.cleaned_data['sort_choice']
    #         search_input = search_form.cleaned_data["search_input"]
    #         if search_choice == 'LOC' or search_choice == 'FOODTYPE':  # search by property
    #             return render(request, 'home/home.html', {'search_form': search_form, 'search_choice': search_choice, 'char_input': search_input,
    #                                                       'shops': search_by_property(search_choice, sort_choice, search_input)})
    #         elif search_choice == 'COMMENT':  # search by content
    #             comments = search_by_comment(search_input)
    #             return render(request, 'home/home.html', {'search_form': search_form, 'comments': comments})
    #         return render(request, 'home/home.html', {'search_form': search_form})
    # search_form = SearchForm()
    locs = [x[0] for x in Shop.objects.count_occurrence('loc')]
    foodtypes = [x[0] for x in Shop.objects.count_occurrence('foodtype')]
    return render(request, 'home/home.html', {'locs': locs, 'foodtypes': foodtypes})


def userprofile(request, username):
    profile = ProfileSite.objects.get(username=username)
    return render(request, 'home/userprofile.html', {'profile': profile })


# def search(request, **search_choices):
#     shops = search_by_property(**search_choices)
#     other_choices = []  # e.g.[{'loc': [西单, 三里屯]}, ...]
#     valid_fields = ['loc', 'foodtype']
#     context = {}
#     if search_choices['search_choice2'] in valid_fields:
#         other_choices = [x[1] for x in Shop.objects.count_occurrence(search_choices['search_choice1'])]


def translate(str):
    if str == 'loc':
        return '商区'
    else:
        return '类别'


def search_by_loc(request, **kwargs):  # e.g.{'loc': '西单', 'foodtype': '泰国菜', 'order_by': taste}
    shops = Shop.objects.all()
    for key, value in kwargs.items():
        if not value == 'all' and not key == 'order_by':
            shops = shops.filter(**{key: value})
    shops = shops.order_by(kwargs['order_by'])
    other_choices = [x[0] for x in Shop.objects.count_occurrence('foodtype')]
    context = {'search_by': 'loc', 'loc': kwargs['loc'], 'foodtype': kwargs['foodtype'],
               'order_by': kwargs['order_by'], 'shops': shops, 'other_choices': other_choices}
    return render(request, 'home/search.html', context)


def search_by_foodtype(request, **kwargs):
    shops = Shop.objects.all()
    for key, value in kwargs.items():
        if not value == 'all' and not key == 'order_by':
            shops = shops.filter(**{key: value})
    shops = shops.order_by(kwargs['order_by'])
    other_choices = [x[0] for x in Shop.objects.count_occurrence('loc')]
    context = {'search_by': 'foodtype', 'loc': kwargs['loc'], 'foodtype': kwargs['foodtype'],
               'order_by': kwargs['order_by'], 'shops': shops, 'other_choices': other_choices}
    return render(request, 'home/search.html', context)

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










