from rest_framework import serializers
from .models import User,MovieID
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from movies.models import Genre
from movies.serializers import GenreSerializer

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username',)



#유저 프로필
class UserProfileSerializer(serializers.ModelSerializer):
    favorite_genres = serializers.PrimaryKeyRelatedField(
    many=True,
    queryset=Genre.objects.all(),
    required=False
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'gender', 'favorite_genres',)  # favorite_genres 필드 추가

# 비밀번호 변경
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['current_password']):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return data

    def validate_new_password(self, value):
        """
        새 비밀번호 유효성 검사
        """
        try:
            password_validation.validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value


# 회원가입 커스텀
class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.CharField(max_length=1)
    favorite_genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Genre.objects.all(),  # Genre 모델에서 선택 가능
        required=False
    )

    def save(self, request):
        user = super().save(request)
        gender_value =  self.validated_data.get('gender')
        favorite_genres = self.validated_data.get('favorite_genres', [])  # 선택된 장르들

        user.gender = gender_value
        user.favorite_genres.set(favorite_genres)  # ManyToManyField에 장르 설정
        user.save()
        return user


# 유저 리스트
class UserListSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)
    favorite_genres = GenreSerializer(many=True, read_only=True)  # 장르를 Serializer로 표시

    class Meta:
        model = User
        fields = (
            'id', 'username', 'followers_count', 'followings_count', 'gender', 'favorite_genres',
        )
