from django.urls import path
from . import views


urlpatterns = [
    path('',views.get_movie_lists),
    path('genres/',views.genre_list),
    path('<int:movie_id>/like/',views.toggle_like_movie),

]