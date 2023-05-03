from rest_framework.test import APITestCase
from home.models import Post, Comment, Vote
from accounts.models import User


class TestPostModel(APITestCase):
    def test_model_str(self):
        user = User.objects.create(staff_id='1271677601', email='deli@email.com', phone_number='09131234567',
                                   username='delaram', is_active=True, is_admin=False)
        post = Post.objects.create(user=user, body='this is first post', slug='firstpost', title='First')
        self.assertEqual(str(post), f'firstpost - {post.updated}')

class TestCommentModel(APITestCase):
    def test_model_str(self):
        user = User.objects.create(staff_id='1271677601', email='deli@email.com', phone_number='09131234567',
                                   username='delaram', is_active=True, is_admin=False)
        post = Post.objects.create(user=user, body='this is first post', slug='firstpost', title='First')
        comment = Comment.objects.create(user=user, post=post, is_reply=False, body='comment', )
        self.assertEqual(str(comment), 'deli@email.com - comment')


class TestVoteModel(APITestCase):
    def test_model_str(self):
        user = User.objects.create(staff_id='1271677601', email='deli@email.com', phone_number='09131234567',
                                   username='delaram', is_active=True, is_admin=False)
        post = Post.objects.create(user=user, body='this is first post', slug='firstpost', title='First')
        vote = Vote.objects.create(user=user, post=post)
        self.assertEqual(str(vote), 'deli@email.com liked firstpost')
