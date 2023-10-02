from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search', NewsSearch.as_view(), name='post_search'),
    path('create', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]