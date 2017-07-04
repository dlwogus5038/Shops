from django.conf.urls import url

from . import views


app_name = 'single_shop'  # namespace
urlpatterns = [
    url(r'^(?P<urlID>[0-9]+)$', views.single_shop, name='single_shop'),
    # ex: /polls/5/
    # url(r'^(?P<id>[0-9]+)/$', views.detail, name='detail'),
]