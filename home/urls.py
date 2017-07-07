from django.conf.urls import url
from . import views, auth_views

app_name = 'home'  # namespace
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/loc/(?P<loc>.+)/(?P<foodtype>.+)/(?P<order_by>.+)/$', views.search_by_loc, name='search-by-loc'),
    url(r'^search/foodtype/(?P<foodtype>.+)/(?P<loc>.+)/(?P<order_by>.+)/$', views.search_by_foodtype, name='search-by-foodtype'),
    url(r'statistics/(?P<loc>.+)/(?P<foodtype>.+)/$', views.show_statistics, name='statistics'),

    # auth
    url(r'^userprofile/(.+)$', views.userprofile, name='userprofile'),
    url(r'^change_profile/$', views.change_profile, name='change_profile'),
    url(r'^delete_friend/(.+)$', views.delete_friend, name='delete_friend'),
    url(r'^delete_comment_user/(.+)$', views.delete_comment_user, name='delete_comment_user'),
    url(r'^delete_comment_shop/(.+)$', views.delete_comment_shop, name='delete_comment_shop'),
    url(r'^requestfriend/(.+)$', views.requestfriend, name='requestfriend'),
    url(r'^makefriend/(.+)$', views.makefriend, name='makefriend'),
    url(r'^collectshop/(.+)$', views.collectshop, name='collectshop'),
    url(r'^cancelshop/(.+)$', views.cancelshop, name='cancelshop'),
    url(r'^ranking-lists/$', views.show_ranking_lists, name='ranking-lists'),
    url(r'^login$', auth_views.login, name='login'),
    url(r'^authenticate$', auth_views.authenticate, name='authenticate'),
    url(r'^signup$', auth_views.signup, name='signup'),
    url(r'^signup/submit$', auth_views.signup_submit, name='signup-submit'),
    url(r'^logout$', auth_views.logout, name='logout'),
]
