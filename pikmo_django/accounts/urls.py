from django.urls import path
from . import views

urlpatterns = [
    path('', views.users_list, name='users_list'),  # 전체 사용자 목록
    path('signup/',views.signup),
    path('liked-movies/',views.get_liked_movies),
    path('profile/<int:user_pk>/', views.user_profile, name='user_profile'),
    path('profile/<int:user_pk>/update/', views.user_profile, name='user_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('<int:user_pk>/follow-list/', views.follow_list, name='follow_list'),  # 특정 사용자가 팔로우한 사람 목록
    path('<int:user_pk>/follower-list/', views.follower_list, name='follower_list'),  # 특정 사용자를 팔로우한 사람 목록
    path('<int:user_pk>/follow/', views.follow, name='follow'),  # 팔로우/언팔로우
    
]
