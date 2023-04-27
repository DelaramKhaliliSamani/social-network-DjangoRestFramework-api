from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer, PostCreateSerializer, CommentSerializer, CommentCreateSerializer, VoteSerializer
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment, Vote
from django.shortcuts import get_object_or_404
from accounts.models import User
from django.http import JsonResponse

class PostCreate(APIView):
    """""
    create a post
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostCreateSerializer
    def post(self, request):
        ser_data = PostCreateSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save(user=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class PostView(APIView):
    """""
    view a particular user posts
    pk = user_id
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = PostSerializer
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        post = Post.objects.filter(user=user)
        srz_data = PostSerializer(instance=post, many=True)
        return Response(data=srz_data.data)
# show all posts, update posts, delete posts
class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    """""
    view all posts
    """""
    def list(self, request):
        srz_data = PostSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)
    """""
    update a post
    pk=post_id
    """""
    def partial_update(self, request, pk=None):
        permission_classes = [IsAuthenticated, ]
        post = get_object_or_404(self.queryset, pk=pk)
        user = post.user
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        srz_data = PostSerializer(instance=post, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save()
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors)
    """""
    delete a post
    pk=post_id
    """""
    def destroy(self, request, pk=None):
        permission_classes = [IsAuthenticated, ]
        post = get_object_or_404(self.queryset, pk=pk)
        user = post.user
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        post.delete()
        return Response({'message': 'post deleted'})
    """""
    create a comment
    pk=post_id
    """""
class CommentCreate(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentCreateSerializer
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        ser_data = CommentCreateSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.save(user=request.user, post=post)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    """""
    show all comments
    """""
    def list(self, request):
        srz_data = CommentSerializer(instance=self.queryset, many=True)
        return Response(data=srz_data.data)
    """""
    update a comment 
    pk = comment_id
    """""
    def partial_update(self, request, pk=None):
        permission_classes = [IsAuthenticated, ]
        comment = get_object_or_404(self.queryset, pk=pk)
        user = comment.user
        post = comment.post
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        srz_data = CommentSerializer(instance=comment, data=request.POST, partial=True)
        if srz_data.is_valid():
            srz_data.save(user=user, post=post)
            return Response(data=srz_data.data)
        return Response(data=srz_data.errors)
    """""
    delete a comment
    pk=comment_id
    """""
    def destroy(self, request, pk=None):
        permission_classes = [IsAuthenticated, ]
        comment = get_object_or_404(self.queryset, pk=pk)
        user = comment.user
        post = comment.post
        if user != request.user:
            return Response({'permission denied': 'you are not the owner'})
        comment.delete()
        return Response({'message': 'comment deleted'})

class VoteView(APIView):
    """""
    like and dislike a post
    pk=post_id
    """""
    permission_classes = [IsAuthenticated, ]
    serializer_class = VoteSerializer
    def get(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        already_liked = Vote.objects.filter(post=post, user=user).first()
        if not already_liked:
            new_like = Vote(post=post, user=user)
            new_like.save()
            follower_count = Vote.objects.filter(user=user).count()
            return JsonResponse({'status': 'Following', 'count': follower_count})
        else:
            already_liked.delete()
            follower_count = Vote.objects.filter(user=user).count()
            return JsonResponse({'status': 'Not following', 'count': follower_count})
        return redirect('/')
