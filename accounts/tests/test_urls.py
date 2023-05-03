from rest_framework.test import APISimpleTestCase
from django.urls import resolve, reverse
from accounts.views import UserRegister, ChangePasswordView, MessageCreate, MessageView, ProfileCreateView, FollowView


class TestUrls(APISimpleTestCase):
    def test_user_register(self):
        url = reverse("accounts:user_register")
        self.assertEqual(resolve(url).func.view_class, UserRegister)
    def test_change_password(self):
        url = reverse("accounts:change-password")
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)
    def test_create_message(self):
        url = reverse("accounts:create_message", args=('1'))
        self.assertEqual(resolve(url).func.view_class, MessageCreate)
    def test_view_message(self):
        url = reverse("accounts:view_message", args=('1'))
        self.assertEqual(resolve(url).func.view_class, MessageView)
    def test_create_profile(self):
        url = reverse("accounts:create_profile")
        self.assertEqual(resolve(url).func.view_class, ProfileCreateView)
    def test_follow(self):
        url = reverse("accounts:follow", args=('1'))
        self.assertEqual(resolve(url).func.view_class, FollowView)

