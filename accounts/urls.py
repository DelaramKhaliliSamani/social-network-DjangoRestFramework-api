from django.urls import path
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'accounts'
urlpatterns = [
	path('register/', views.UserRegister.as_view()),
	path('message/create/<int:pk>/', views.MessageCreate.as_view()),
	path('message/view/<int:pk>/', views.MessageView.as_view()),
	path('profile/create/', views.ProfileCreateView.as_view()),
	path('follow/<int:pk>/', views.FollowView.as_view()),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

router = routers.SimpleRouter()
router.register('user', views.UserViewSet)
router.register('profile', views.ProfileViewSet)
router.register('message', views.MessageSetView)
urlpatterns += router.urls