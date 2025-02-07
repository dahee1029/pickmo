from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_pk>/', views.article_detail),
    path('articles/<int:article_pk>/comments/', views.comment_create_list),
    # path('comments/<int:article_pk>/',views.comment_list),
    path('comments/<int:comment_pk>/',views.comment_detail),

]