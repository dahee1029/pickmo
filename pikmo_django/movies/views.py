from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import requests
from rest_framework.decorators import api_view, permission_classes
from .models import Movie, Genre
from .serializers import MovieListsSerializer,GenreSerializer
from accounts.models import MovieID
from django.db.models import Prefetch


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like_movie(request, movie_id):
    try:
        # MovieID가 없으면 생성
        movie_obj, created = MovieID.objects.get_or_create(movie_id=movie_id)

        # 현재 사용자의 liked_movies에서 상태 확인
        user = request.user
        if movie_obj in user.liked_movies.all():
            user.liked_movies.remove(movie_obj)  # 좋아요 취소
            return JsonResponse({"message": "좋아요 취소 완료", "liked": False})
        else:
            user.liked_movies.add(movie_obj)  # 좋아요 추가
            return JsonResponse({"message": "좋아요 추가 완료", "liked": True})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
def genre_list(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return JsonResponse(serializer.data, safe=False)  # safe=False 추가


# 영화 데이터를 특정 API URL에서 가져와 DB에 저장하는 함수
def fetch_movie_data(api_url, headers):
    try:
        # API 데이터 가져오기
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        popular_data = response.json().get('results', [])
        
        # 각 영화의 상세 정보를 가져오기
        for movie in popular_data:
            movie_id = movie.get('id')
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=en-US&append_to_response=credits'
            detail_response = requests.get(detail_url, headers=headers)
            detail_response.raise_for_status()
            detail_data = detail_response.json()
            
            # 장르 이름 추출
            genres = detail_data.get('genres', [])
            genre_names = ', '.join([genre['name'] for genre in genres])
            
            # 데이터 저장
            Movie.objects.update_or_create(
                id=movie_id,
                defaults={
                    'title': movie.get('title'),
                    'poster_path': f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}",
                    'genre': genre_names,  # 장르 이름 저장
                    'release_date': movie.get('release_date'),
                    'overview': movie.get('overview'),
                    'runtime': detail_data.get('runtime'),
                    'budget': detail_data.get('budget'),
                    'revenue': detail_data.get('revenue'),
                }
            )
        return True  # 성공 시 True 반환
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return False  # 실패 시 False 반환


# 여러 카테고리의 영화를 가져오는 뷰
@api_view(['GET'])
def get_movie_lists(request):
    # 카테고리 목록
    movie_categories = ['now_playing', 'popular', 'top_rated', 'upcoming']
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNTU5OTRmN2QwZWI3MGI4OWE5MWJmYTFjN2ZhODRhOSIsIm5iZiI6MTczMTg5NzA4Mi4yNTkyMTEsInN1YiI6IjY2Mjg3OTRmYTM5ZDBiMDE3MDQ3YWQ0MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.SMxiiBJThqDqIyT847Q70HQMFHO82_izerzjZGNpDwY"
    }
    
    # 모든 카테고리 데이터를 순차적으로 가져옴
    for category in movie_categories:
        api_url = f"https://api.themoviedb.org/3/movie/{category}?language=en-US&page=1"
        success = fetch_movie_data(api_url, headers)
        if not success:
            return JsonResponse({'error': f"Failed to fetch data for category: {category}"}, status=500)
    
    # 저장된 데이터를 직렬화하여 반환
    saved_movies = Movie.objects.all()  # 모든 저장된 영화 가져오기
    serializer = MovieListsSerializer(saved_movies, many=True)
    return JsonResponse(serializer.data, safe=False, status=200)


# # movies/views.py
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_movie_detail(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return JsonResponse({"error": "영화를 찾을 수 없습니다."}, status=404)

    is_liked = request.user in movie.liked_by.all()  # 현재 사용자가 좋아요 했는지 확인
    data = {
        "movie": {
            "id": movie.id,
            "title": movie.title,
            "poster_path": movie.poster_path,
            "release_date": movie.release_date,
            "runtime": movie.runtime,
            "vote_average": movie.vote_average,
            "genres": [{"id": g.id, "name": g.name} for g in movie.genres.all()],
            "overview": movie.overview,
        },
        "is_liked": is_liked,
    }
    return JsonResponse(data)
