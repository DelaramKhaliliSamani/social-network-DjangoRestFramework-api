from django.urls import path, include
from . import views

app_name = 'manuals'
urlpatterns = [
	path('web/', views.WebManualView.as_view(), name='web_manual'),
    path('mobile/', views.MobileManualView.as_view(), name='mobile_manual'),
    path('admin/', views.AdminManualView.as_view(), name='mobile_manual'),
  ]
