from rest_framework.test import APISimpleTestCase
from django.urls import resolve, reverse
from home.views import PostCreate, PostView, CommentCreate, VoteView

class TestUrls(APISimpleTestCase):
    def test_post_create(self):
        url = reverse("home:post_create")
        self.assertEqual(resolve(url).func.view_class, PostCreate)


    def test_post_view(self):
        url = reverse("home:post_view", args=('1'))
        self.assertEqual(resolve(url).func.view_class, PostView)


    def test_comment_create(self):
        url = reverse("home:comment_create", args=('2'))
        self.assertEqual(resolve(url).func.view_class, CommentCreate)

    def test_like(self):
        url = reverse("home:like", args=('1'))
        self.assertEqual(resolve(url).func.view_class, VoteView)