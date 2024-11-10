from django.http import HttpResponse
from django.urls import path, include
from .views import get_token, GoodsListView, NewGoodView, home


urlpatterns = [
    path('get_token/', get_token, name='get_token'),
    path('goods/', GoodsListView.as_view(), name='goods_list'),
    path('new_good/', NewGoodView.as_view(), name='new_good'),
    path('', home, name='home'),
]
