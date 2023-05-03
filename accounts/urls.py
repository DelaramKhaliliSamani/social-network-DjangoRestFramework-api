from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'accounts'
urlpatterns = [
	path('register/', views.UserRegister.as_view(), name='user_register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
	path('message/create/<int:pk>/', views.MessageCreate.as_view(), name='create_message'),
	path('message/view/<int:pk>/', views.MessageView.as_view(), name='view_message'),
	path('profile/create/', views.ProfileCreateView.as_view(), name='create_profile'),
	path('follow/<int:pk>/', views.FollowView.as_view(), name='follow'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet, basename='user_set')
router.register('profile', views.ProfileViewSet, basename='profile_set')
router.register('message', views.MessageSetView, basename='message_set')
urlpatterns += router.urls