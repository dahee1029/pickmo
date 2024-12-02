from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre

class MovieID(models.Model):
    movie_id = models.IntegerField(unique=True) 

class User(AbstractUser):
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers'
    )
    gender = models.CharField(
        max_length=1,
        choices=(
            ('f', '여성'),
            ('m', '남성'),
        ),
    )
    favorite_genres = models.ManyToManyField(Genre, related_name='users', blank=True)
    liked_movies = models.ManyToManyField(
        MovieID,  # ForeignKey에서 ManyToManyField로 수정
        related_name='liked_by',
        blank=True
    )
