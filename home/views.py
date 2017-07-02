from django.shortcuts import render

# Create your views here.
from .models import Shop, Comment
from .forms import SearchForm
import json


def home(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_choice = search_form.cleaned_data['search_choice']
            sort_choice = search_form.cleaned_data['sort_choice']
            return render(request, 'home/home.html', {'search_form': search_form})
    search_form = SearchForm()
    return render(request, 'home/home.html', {'search_form': search_form})

'''def search(request):
    if request.method == 'POST':
        search_choice_form = SearchChoiceForm(request.POST)
        if search_choice_form.is_valid():
            search_choice = search_choice_form.cleaned_data['search_choice']
            sort_choice = search_choice_form.cleaned_data['sort_choice']
            if search_choice == 'LOC' or search_choice == 'FOODTYPE':
                search_by_property(request, search_choice, sort_choice)
            elif search_choice == 'COMMENT':
                search_by_comment(request, sort_choice)
    return render(request, 'home/home.html')

def search_by_property(request, search_choice, sort_choice):
    if request.method == 'POST':
        char_input_form = CharForm(request.POST)
        if char_input_form.is_valid():
            char_input = char_input_form.cleaned_data['char_input']
            shops = []  # show shop information
            if search_choice == 'LOC':
                shops = Shop.objects.filter(loc=char_input).order_by('-' + sort_choice.lower())
            elif search_choice == 'FOODTYPE':
                shops = Shop.objects.filter(foodtype=char_input).order_by('-' + sort_choice.lower())
            return render(request, 'home/home.html',
                          {'char_input_form': char_input_form, 'char_input': char_input, 'shops': shops})
    char_input_form = CharForm()
    return render(request, 'home/home.html', {'char_input_form': char_input_form})'''


def show_statistics(request, search_choice, char_input):
    shops = []
    order_by = 'foodtype'
    if search_choice == 'LOC':
        shops = Shop.objects.filter(loc=char_input)
    elif search_choice == 'FOODTYPE':
        shops = Shop.objects.filter(foodtype=char_input)
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


def search_by_comment(request, sort_choice):
    if request.method == "POST":
        text_input_form = TextForm(request.POST)
        if text_input_form.is_valid():
            return render(request, 'home/home.html', {'text_input_form': text_input_form})
    text_input_form = TextForm()
    return render(request, 'home/home.html', {'text_input_form': text_input_form})
