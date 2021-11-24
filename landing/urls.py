from . import views
from django.urls import path

urlpatterns = [
   path('', views.home, name='article_list'),
   path('create_article', views.create_article, name='article_create'),
   path('<slug>', views.article_detail, name='article_detail'),
   path('<slug>/edit', views.edit_article, name='edit_article'),
   path('<slug>/delete', views.delete_article, name='delete_article'),
   path('<slug>/likes', views.like_article, name='like_article'),
   path('<slug>/dislikes', views.dislike_article, name='dislike_article'),
   path('<slug>/comment/<pk>/delete', views.delete_comment, name='delete_comment'),
   path('<slug>/comment/<pk>/edit', views.edit_comment, name='edit_comment')
]
