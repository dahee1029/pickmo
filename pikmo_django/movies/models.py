from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # settings.AUTH_USER_MODEL을 가져오기 위해 필요
# Create your models here.
# class Movie(models.Model):
    #Popular에 있는 정보들
    # id=models.IntegerField(primary_key=True) #기본키로 설정
    # title=models.CharField(max_length=250) #제목
    # poster_path=models.TextField() #포스터 이미지 url
    # genre = models.CharField(max_length=255) #장르
    # release_date=models.DateField() #개봉일
    # overview=models.TextField() #줄거리


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # 영화 ID
    title = models.CharField(max_length=255)  # 영화 제목
    poster_path = models.URLField(null=True, blank=True)  # 포스터 경로
    genre = models.TextField(null=True, blank=True)  # 장르
    release_date = models.DateField(null=True, blank=True)  # 개봉일
    overview = models.TextField(null=True, blank=True)  # 영화 줄거리
    runtime = models.IntegerField(null=True, blank=True)  # 상영 시간
    # director = models.CharField(max_length=255, null=True, blank=True)  # 감독 이름
    budget = models.BigIntegerField(null=True, blank=True)  # 제작 비용
    revenue = models.BigIntegerField(null=True, blank=True)  # 수익
    liked_by = models.ManyToManyField(
        'accounts.User',
        related_name='liked_movies_set',  
        blank=True
    )
    
class Genre(models.Model):
    id = models.IntegerField(primary_key=True)  # TMDB API의 고유 ID 사용
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name