from django.shortcuts import render

# Create your views here.
from .models import Shop, Comment
from .forms import SearchForm
from django import forms
import json


def home(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_choice = search_form.cleaned_data['search_choice']
            sort_choice = search_form.cleaned_data['sort_choice']
            char_input = search_form.cleaned_data["search_input"]
            if search_choice == 'LOC' or search_choice == 'FOODTYPE':
                return render(request, 'home/home.html', {'search_form': search_form, 'search_choice': search_choice, 'char_input': char_input,
                                                          'shops': search_by_property(search_choice, sort_choice, char_input)})
            elif search_choice == 'COMMENT':
                return render(request, 'home/home.html', {'search_form': search_form})
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
    return render(request, 'home/home.html')'''


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


'''def search_by_comment(request, sort_choice):
    if request.method == "POST":
        text_input_form = TextForm(request.POST)
        if text_input_form.is_valid():
            return render(request, 'home/home.html', {'text_input_form': text_input_form})
    text_input_form = TextForm()
    return render(request, 'home/home.html', {'text_input_form': text_input_form})'''
