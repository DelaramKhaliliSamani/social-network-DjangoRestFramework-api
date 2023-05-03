from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from django.urls import reverse
from accounts.models import User
from home.models import Post, Comment, Vote
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.views import TokenObtainPairView



class TestCreatePostView(APITestCase):
    def setUp(self):
        self.user=User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' )
        self.client.force_authenticate(user=self.user)
    def test_post_create_POST_valid(self):
        response = self.client.post(reverse('home:post_create'), data={'user':self.user, 'body':'hii', 'slug':'hhhh', 'title':'hii'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_create_POST_invalid(self):
        response = self.client.post(reverse('home:post_create'),
                                    data={'user': self.user, 'body': '', 'slug': 'hhhh', 'title': 'hii'})
        self.assertEqual(response.status_code, 400)

class TestPostSetView(APITestCase):
    def setUp(self):
        self.user=User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.user)
        Post.objects.create(user=self.user, body='hi', slug='hhh', title='first post')
    def test_post_set_list(self):
        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)

    def test_post_set_update(self):
        response = self.client.patch('/post/1')
        self.assertEqual(response.status_code, 301)

    def test_post_set_delete(self):
        response = self.client.delete('/post/1')
        self.assertEqual(response.status_code, 301)

    def test_user_posts(self):
        response = self.client.get('/post/view/1/')
        self.assertEqual(response.status_code, 200)

class TestCreateCommentView(APITestCase):
    def setUp(self):
        self.user=User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.post=Post.objects.create(user=self.user, body='hi', slug='hhh', title='first post')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' )
        self.client.force_authenticate(user=self.user)

    def test_comment_create_POST_valid(self):
        response = self.client.post('/comment/create/1/', data={'user':self.user, 'post':self.post, 'is_reply':False, 'body':'first comment'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_post_create_POST_invalid(self):
        response = self.client.post('/comment/create/1/', data={'user':self.user, 'post':self.post, 'is_reply':False, 'body':''})
        self.assertEqual(response.status_code, 400)

class TestCommentSetView(APITestCase):
    def setUp(self):
        self.user=User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.user)
        self.post = Post.objects.create(user=self.user, body='hi', slug='hhh', title='first post')
        self.comment = Comment.objects.create(user=self.user, post=self.post, is_reply=False, body='first comment')
    def test_comment_set_list(self):
        response = self.client.get('/comment/')
        self.assertEqual(response.status_code, 200)

    def test_comment_set_update(self):
        response = self.client.patch('/comment/1/')
        self.assertEqual(response.status_code, 200)


    def test_comment_set_delete(self):
        response = self.client.delete('/comment/1')
        self.assertEqual(response.status_code, 301)


class TestvoteView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567',
                                             username='delaram', password='1234')
        self.post = Post.objects.create(user=self.user, body='pooost', slug='ppp', title='the post')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.user)

    def test_dislike(self):
        Vote.objects.create(user=self.user, post=self.post)
        response = self.client.get('/like/1/')
        self.assertEqual(response.status_code, 200)

    def test_like(self):
        response = self.client.get('/like/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Vote.objects.count(), 1)