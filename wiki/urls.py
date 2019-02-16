from django.urls import path

from .views import (
    WikiArticleView,
    WikiArticleCreateView,
    WikiArticleEditView,
    WikiHomeView,
    WikiSearchView,
    WikiTagView,
)


urlpatterns = [

    path('article/create/',
        WikiArticleCreateView.as_view(),
        name='wiki-article-create'),

    path('article/<int:pk>/edit/',
        WikiArticleEditView.as_view(),
        name='wiki-article-edit'),

    path('article/<str:slug>/',
        WikiArticleView.as_view(),
        name='wiki-article'),

    path('tag/<str:slug>/',
        WikiTagView.as_view(),
        name='wiki-tag'),

    path('search/',
        WikiSearchView.as_view(),
        name='wiki-search'),

    path('',
        WikiHomeView.as_view(),
        name='wiki-index'),
]
