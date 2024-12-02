from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserListSerializer, CustomRegisterSerializer,ChangePasswordSerializer,UserProfileSerializer
from movies.serializers import UserLikedMoviesSerializer
from .models import User
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch  # 추가
from movies.models import Genre
User = get_user_model()



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_liked_movies(request):
    user = request.user

    # liked_movies가 MovieID 객체에 대한 ForeignKey라면 아래처럼 작성
    liked_movie_ids = user.liked_movies.values_list('movie_id', flat=True)
    
    return JsonResponse({"liked_movies": list(liked_movie_ids)})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    현재 로그인된 사용자의 비밀번호를 변경하는 API
    """
    user = request.user  # 현재 로그인된 사용자 가져오기

    # context로 request를 전달
    serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        # 현재 비밀번호 확인
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({"error": "현재 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 새 비밀번호 설정
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#커스텀 회원가입
@api_view(['POST'])
def signup(request):
    """
    회원가입을 처리하는 API 뷰
    """
    if request.method == 'POST':
        # 사용자 정보를 담은 커스텀 직렬화 객체 사용
        serializer = CustomRegisterSerializer(data=request.data)

        # 유효성 검사
        if serializer.is_valid():
            # serializer.save()가 호출되면 `CustomRegisterSerializer`의 save 메서드가 실행됩니다.
            user = serializer.save(request)

            # 사용자가 성공적으로 등록되었으면 Token 생성
            token, created = Token.objects.get_or_create(user=user)
            
            # 응답 데이터
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'token': token.key,
                'gender': user.gender,  # Gender도 포함
            }

            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
# def user_profile(request, user_pk):
#     """
#     특정 사용자(user_pk)의 프로필 정보를 반환하거나 수정하는 API
#     """
#     try:
#         user = get_object_or_404(User, pk=user_pk)  # user_pk로 사용자 조회
#     except User.DoesNotExist:
#         return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

#     # GET 요청: 프로필 데이터 반환
#     if request.method == 'GET':
#         data = {
#             "id": user.id,
#             "username": user.username,
#             "gender": user.gender,
#             "email": user.email,
#             "followers_count": user.followers.count(),
#             "followings_count": user.followings.count(),
#             "liked_movies": UserLikedMoviesSerializer(user).data['liked_movies'],  # 좋아요 목록 추가
#         }
#         return Response(data, status=status.HTTP_200_OK)

#     # PUT 요청: 프로필 데이터 수정
#     elif request.method == 'PUT':
#         # 요청에서 수정할 데이터 추출
#         username = request.data.get('username', user.username)
#         email = request.data.get('email', user.email)
#         gender = request.data.get('gender', user.gender)

#         # 수정된 데이터로 사용자 정보 업데이트
#         user.username = username
#         user.email = email
#         user.gender = gender
#         user.save()  # 변경사항 저장

#         # 수정된 데이터 반환
#         data = {
#             "id": user.id,
#             "username": user.username,
#             "gender": user.gender,
#             "email": user.email,
#             "followers_count": user.followers.count(),
#             "followings_count": user.followings.count(),
#         }
#         return Response(data, status=status.HTTP_200_OK)
# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
# def user_profile(request, user_pk):
#     """
#     특정 사용자(user_pk)의 프로필 정보를 반환하거나 수정하는 API
#     """
#     user = get_object_or_404(
#         User.objects.prefetch_related(
#             Prefetch('followers'), Prefetch('followings'), Prefetch('liked_movies')
#         ),
#         pk=user_pk
#     )

#     # GET 요청: 프로필 데이터 반환
#     if request.method == 'GET':
#         data = {
#             "id": user.id,
#             "username": user.username,
#             "gender": user.gender,
#             "email": user.email,
#             "followers_count": user.followers.count(),
#             "followings_count": user.followings.count(),
#             "liked_movies": UserLikedMoviesSerializer(user.liked_movies.all(), many=True).data,
#         }
#         return Response(data, status=status.HTTP_200_OK)

#     # PUT 요청: 프로필 데이터 수정
#     elif request.method == 'PUT':
#         serializer = UserProfileSerializer(user, data=request.data, partial=True)  # 부분 업데이트 허용
#         if serializer.is_valid():
#             serializer.save()
#             # 수정된 데이터 반환
#             data = {
#                 "id": user.id,
#                 "username": user.username,
#                 "gender": user.gender,
#                 "email": user.email,
#                 "followers_count": user.followers.count(),
#                 "followings_count": user.followings.count(),
#                 "liked_movies": UserLikedMoviesSerializer(user.liked_movies.all(), many=True).data,
#             }
#             return Response(data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def user_profile(request, user_pk):
    """
    특정 사용자(user_pk)의 프로필 정보를 반환하거나 수정하는 API
    """
    user = get_object_or_404(
        User.objects.prefetch_related(
            Prefetch('followers'), 
            Prefetch('followings'), 
            Prefetch('liked_movies'),  # MovieID 모델과의 관계
            Prefetch('favorite_genres')
        ),
        pk=user_pk
    )

    # GET 요청: 프로필 데이터 반환
    if request.method == 'GET':
        data = {
            "id": user.id,
            "username": user.username,
            "gender": user.gender,
            "email": user.email,
            "followers_count": user.followers.count(),
            "followings_count": user.followings.count(),
            "liked_movies": [movie.movie_id for movie in user.liked_movies.all()],  # 수정된 부분
            "favorite_genres": [genre.name for genre in user.favorite_genres.all()],
        }
        return Response(data, status=status.HTTP_200_OK)

    # PUT 요청: 프로필 데이터 수정
    elif request.method == 'PUT':
        # JSON 데이터에서 선호 장르 처리
        favorite_genres_names = request.data.pop("favorite_genres", [])
        serializer = UserProfileSerializer(user, data=request.data, partial=True)  # 부분 업데이트 허용
        
        if serializer.is_valid():
            serializer.save()
            # 선호 장르 업데이트
            favorite_genres = Genre.objects.filter(name__in=favorite_genres_names)
            if favorite_genres.exists():  # 장르가 유효할 경우에만 업데이트
                user.favorite_genres.set(favorite_genres)
            else:
                user.favorite_genres.clear()  # 유효하지 않을 경우 기존 장르 초기화
            
            # 수정된 데이터 반환
            data = {
                "id": user.id,
                "username": user.username,
                "gender": user.gender,
                "email": user.email,
                "followers_count": user.followers.count(),
                "followings_count": user.followings.count(),
                "liked_movies": [movie.movie_id for movie in user.liked_movies.all()],  # 수정된 부분
                "favorite_genres": [genre.name for genre in user.favorite_genres.all()],
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def users_list(request):
    users = User.objects.all()
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def follow(request, user_pk):
    try:
        you = User.objects.get(pk=user_pk)  # 팔로우 대상
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    me = request.user  # 현재 로그인한 사용자

    if me == you:
        return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    if me in you.followers.all():
        you.followers.remove(me)  # 언팔로우
        is_following = False
    else:
        you.followers.add(me)  # 팔로우
        is_following = True

    data = {
        "is_following": is_following,
        "followers_count": you.followers.count(),
        "followings_count": me.followings.count(),
    }
    return Response(data, status=status.HTTP_200_OK)



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def follow_list(request, user_pk=None):
    """특정 사용자가 팔로우한 사용자 목록 반환"""
    try:
        user = User.objects.get(pk=user_pk) if user_pk else request.user
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    followings = user.followings.all()  # 특정 유저가 팔로우한 사람들
    serializer = UserListSerializer(followings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def follower_list(request, user_pk=None):
    """특정 사용자를 팔로우한 사용자 목록 반환"""
    try:
        user = User.objects.get(pk=user_pk) if user_pk else request.user
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    followers = user.followers.all()  # 특정 유저를 팔로우한 사람들
    serializer = UserListSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)