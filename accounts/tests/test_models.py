from rest_framework.test import APITestCase
from accounts.models import User, Relation, DirectMessage

class TestUserModel(APITestCase):
    def test_model_str(self):
        user = User.objects.create(staff_id='1271677601', email='deli@email.com', phone_number='09131234567',
                                   username='delaram', is_active=True, is_admin=False)
        self.assertEqual(str(user), 'deli@email.com')

    def test_is_staff(self):
        user = User.objects.create(staff_id='1271677601', email='deli@email.com', phone_number='09131234567',
                                   username='delaram', is_active=True, is_admin=True)
        self.assertTrue(user.is_admin, True)


class TestRelationModel(APITestCase):

    def test_model_str(self):
        from_user = User.objects.create(staff_id='9876543210', email='sam@email.com', phone_number='09101234567',
                                        username='sam', is_active=True, is_admin=True)

        to_user = User.objects.create(staff_id='1271699601', email='jack@email.com', phone_number='09121234567',
                                      username='jack', is_active=True, is_admin=True)
        relation = Relation.objects.create(from_user=from_user, to_user=to_user)
        self.assertEqual(str(relation), 'sam@email.com following jack@email.com')


class TestDirectMessageModel(APITestCase):

    def test_model_str(self):
        from_user = User.objects.create(staff_id='9876543210', email='sam@email.com', phone_number='09101234567',
                                        username='sam', is_active=True, is_admin=True)

        to_user = User.objects.create(staff_id='1271699601', email='jack@email.com', phone_number='09121234567',
                                      username='jack', is_active=True, is_admin=True)
        message = DirectMessage.objects.create(from_user=from_user, to_user=to_user, body='hi there', doc=None)
        self.assertEqual(str(message), 'sam@email.com seding message to jack@email.com')