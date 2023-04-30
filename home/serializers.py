from rest_framework import serializers
from .custom_relational_fields import UserEmailNameRelationalField
from .models import Post, Comment, Vote


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('body',)


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    votes = serializers.SerializerMethodField()
    user =UserEmailNameRelationalField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_votes(self, obj):
        result = obj.pvotes.all()
        return VoteSerializer(instance=result, many=True).data

    def get_comments(self, obj):
         result = obj.pcomments.all()
         return CommentSerializer(instance=result, many=True).data

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields =('body',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields ='__all__'


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
