from rest_framework import serializers
from .models import Article,Comment

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'content','movie_id','user_id')


class ArticleSerializer(serializers.ModelSerializer):
    class CommentDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model=Comment
            fields=('id','content',)
    comment_set=CommentDetailSerializer(many=True,read_only=True)
    comment_count=serializers.IntegerField(source='comment_set.count',read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):
    # 댓글 작성자의 username 포함
    username = serializers.CharField(source='user.username', read_only=True)
    class ArticleInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model=Article
            fields=('title','id',)
    article=ArticleInfoSerializer(read_only=True)
    

    class Meta:
        model=Comment
        fields='__all__'
        read_only_fields = ('user',)