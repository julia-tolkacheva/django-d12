from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreateView, PostUpdateView, PostDeleteView, SubscribeView
from .views import upgrade_acc

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
    path('search', cache_page(60*5)(NewsSearch.as_view()), name='post_search'),
    path('create', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/<int:pk>', SubscribeView.as_view(), name='subscribe'),
    path('upgrade', upgrade_acc, name='upgrade'),
]