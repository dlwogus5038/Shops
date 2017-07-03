from django.shortcuts import render

# Create your views here.
from .models import Shop, Comment
from .forms import SearchForm
import json
import jieba
import gensim
from pre_process.generate_index_file_defs import get_stop_words


dictionary_file = 'pre_process/comment_dictionary.dict'
lsi_file = 'pre_process/comment_lsi.lsi'
index_file = 'pre_process/comment_index.index'
shop_ids_file = 'pre_process/shop_ids.txt'
comment_file = 'pre_process/comments.txt'
stop_words_file = 'pre_process/stop_words.txt'


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
                comments, shops = search_by_comment(search_input, sort_choice)
                return render(request, 'home/home.html', {'search_form': search_form,
                                                          'comments': comments, 'shops': shops})
            return render(request, 'home/home.html', {'search_form': search_form})
    search_form = SearchForm()
    return render(request, 'home/home.html', {'search_form': search_form})


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


def search_by_comment(search_input, sort_choice):
    # pre-procession
    words = jieba.cut(search_input)
    stop_words_list = get_stop_words(stop_words_file)
    words = [word for word in words if not word in stop_words_list]
    dictionary = gensim.corpora.Dictionary.load(dictionary_file)
    lsi = gensim.models.LsiModel.load(lsi_file)
    query_lsi = lsi[dictionary.doc2bow(words)]

    index = gensim.similarities.Similarity.load(index_file)
    sims = index[query_lsi]
    max_shop_num = 50
    sims = sorted(enumerate(sims), key=lambda item: -item[1])[:max_shop_num]

    comments = []
    with open(comment_file) as f:
       lines = f.readlines()
       comments = [lines[item[0]] for item in sims]
    shop_ids = []
    with open(shop_ids_file) as f:
       lines = f.readlines()
       shop_ids = [int(lines[item[0]]) for item in sims]
    shops = Shop.objects.filter(pk__in=shop_ids).order_by(sort_choice.lower())
    return comments, shops








