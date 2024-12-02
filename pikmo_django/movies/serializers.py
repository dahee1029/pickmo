from rest_framework import serializers
from .models import Movie,Genre
from django.contrib.auth.models import User

# 영화 장르
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class MovieListsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields="__all__"


# movies/serializers.py
class UserLikedMoviesSerializer(serializers.ModelSerializer):
    liked_movies = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'liked_movies']
