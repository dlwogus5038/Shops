from django.conf.urls import url
from .import views

app_name = 'home'  # namespace
urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url(r'^search-by-property/(?P<search_choice>LOC|FOODTYPE)/(?P<sort_choice>TASTE|SERVICE|ENVI)/$', views.search_by_property, name='search-by-property'),
    url(r'^statistics/(?P<search_choice>LOC|FOODTYPE)/(?P<char_input>.+)/$', views.show_statistics, name='statistics'),
    # url(r'^search-by-comment/(?P<sort_choice>TASTE|SERVICE|ENVI)/$', views.search_by_comment, name='search-by-comment'),
]
