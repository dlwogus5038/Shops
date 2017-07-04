from django.conf.urls import url

from . import views


app_name = 'single_shop'  # namespace
urlpatterns = [
    url(r'^$', views.single_shop, name='single_shop'),
]