from django.urls import path
from . import views
from rest_framework import routers



app_name = 'home'
urlpatterns = [
    path('post/create/', views.PostCreate.as_view(), name='post_create'),
    path('post/view/<int:pk>/', views.PostView.as_view(), name='post_view'),
    path('comment/create/<int:pk>/', views.CommentCreate.as_view(), name='comment_create'),
    path('like/<int:pk>/', views.VoteView.as_view(), name='like'),

]
router = routers.SimpleRouter()
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)
urlpatterns += router.urls
