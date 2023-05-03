from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from django.urls import reverse
from accounts.models import User, DirectMessage, Profile, Relation
from accounts.views import UserViewSet
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.views import TokenObtainPairView


class TestUserRegisterView(APITestCase):
    def setUp(self):
        self.client = APIClient()
    def test_user_register_POST_valid(self):
        response = self.client.post(reverse('accounts:user_register'), data={'staff_id':'1271677601', 'email':'de@email.com', 'phone_number':'09131234567', 'username':'delaram', 'password':'1234', 'password2':'1234'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(reverse('accounts:user_register'), data={'staff_id':'1271677601', 'email':'invalid_email', 'phone_number':'09131234567', 'username':'delaram', 'password':'1234', 'password2':'1234'})
        self.assertEqual(response.status_code, 400)


class TestUserView(APITestCase):
    def setUp(self):
        self.user=User.objects.create(staff_id='1271677601', email='deli@email.com', phone_number='09131234567',
                                   username='delaram', is_active=True, is_admin=False, password='1234')
        self.factory= APIRequestFactory()
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.user)


    def test_user_authenticated(self):
        request = self.factory.get('/accounts/user/')
        force_authenticate(request, user=self.user)
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)


    def test_user_annonymous(self):
        request = self.factory.get('/accounts/user/')
        request.user = AnonymousUser
        response = UserViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 401)

    def test_user_set_list(self):
        response = self.client.get('/accounts/user/')
        self.assertEqual(response.status_code, 200)

    def test_user_set_retrieve(self):
        response = self.client.get('/accounts/user/1')
        self.assertEqual(response.status_code, 301)

    def test_user_set_update(self):
        response = self.client.patch('/accounts/user/1', {'username':'jack'})
        self.assertEqual(response.status_code, 301)

    def test_user_set_delete(self):
        response = self.client.delete('/accounts/user/1')
        self.assertEqual(response.status_code, 301)


class TestCreateMessageView(APITestCase):
    def setUp(self):
        self.from_user=User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.to_user=User.objects.create(staff_id='9876543210', email='jack@email.com', phone_number='09121234567', username='jack', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' )
        self.client.force_authenticate(user=self.from_user)

    def test_message_create_POST_valid(self):
        response = self.client.post('/accounts/message/create/1/', data={'body':'first comment'})
        response.from_user=self.from_user
        response.to_user=self.to_user
        self.assertEqual(response.status_code, 201)
        self.assertEqual(DirectMessage.objects.count(), 1)

    def test_message_create_POST_invalid(self):
        response = self.client.post('/accounts/message/create/1/', data={'body': ''})
        response.from_user = self.from_user
        response.to_user = self.to_user
        self.assertEqual(response.status_code, 400)

class TestMessageSetView(APITestCase):
    def setUp(self):
        self.from_user = User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567',
                                             username='delaram', password='1234')
        self.to_user = User.objects.create(staff_id='9876543210', email='jack@email.com', phone_number='09121234567',
                                           username='jack', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.from_user)
    def test_message_view(self):
        response = self.client.get('/accounts/message/view/2/')
        self.assertEqual(response.status_code, 200)

    def test_message_set_update(self):
        message = DirectMessage.objects.create(from_user=self.from_user, to_user=self.to_user, body='hiii')
        response = self.client.patch('/accounts/message/1/', {'body':'hello'})
        self.assertEqual(response.status_code, 200)


    def test_message_set_delete(self):
        message = DirectMessage.objects.create(from_user=self.from_user, to_user=self.to_user, body='hiii')
        response = self.client.delete('/accounts/message/1/')
        self.assertEqual(response.status_code, 200)


class TestCreateProfileView(APITestCase):
    def setUp(self):
        self.user=User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' )
        self.client.force_authenticate(user=self.user)

    def test_profile_create_POST_valid(self):
        response = self.client.post('/accounts/profile/create/', data={'bio': 'rfsfs' })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Profile.objects.count(), 1)

class TestProfileSetView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567',
                                             username='delaram', password='1234')
        self.profile =Profile.objects.create(user=self.user, bio='cdsd')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.user)
    def test_profile_list(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_retrieve(self):
        response = self.client.get('/accounts/profile/1/')
        self.assertEqual(response.status_code, 200)

    def test_profile_set_update(self):
        response = self.client.patch('/accounts/profile/1/', {'bio':'hello'})
        self.assertEqual(response.status_code, 200)

class TestChangePasswordView(APITestCase):
    def setUp(self):
        self.user = User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567', username='delaram', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.user)

    def test_password_change_PUT_invalid(self):
        response = self.client.put('/accounts/change-password/', data={'old_password':'12345', 'new_password':'123456'})
        self.assertEqual(response.status_code, 400)

class TestFollowView(APITestCase):
    def setUp(self):
        self.from_user = User.objects.create(staff_id='1271677601', email='de@email.com', phone_number='09131234567',
                                             username='delaram', password='1234')
        self.to_user = User.objects.create(staff_id='9876543210', email='jack@email.com', phone_number='09121234567',
                                           username='jack', password='1234')
        self.token = TokenObtainPairView()
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        self.client.force_authenticate(user=self.from_user)

    def test_unfollow(self):
        Relation.objects.create(from_user=self.from_user, to_user=self.to_user)
        response = self.client.get('/accounts/follow/2/')
        self.assertEqual(response.status_code, 200)

    def test_follow(self):
        response = self.client.get('/accounts/follow/2/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Relation.objects.count(), 1)
