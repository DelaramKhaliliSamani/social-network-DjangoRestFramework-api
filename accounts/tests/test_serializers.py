from rest_framework.test import APITestCase
from accounts.serializers import UserRegisterSerializer

class TestRegistrationSerializer(APITestCase):
    def test_valid_data(self):
        srz_data = UserRegisterSerializer(data={'staff_id':'1271677601', 'email':'deli@gmail.com', 'phone_number':'09131234567',
                                                'username':'delaram', 'password':'1234', 'password2':'1234'})
        self.assertTrue(srz_data.is_valid())

    def test_empty_data(self):
        srz_data = UserRegisterSerializer(data={})
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 6)

    def test_invalid_username(self):
        srz_data = UserRegisterSerializer(data={'staff_id':'1271677601', 'email':'deli@gmail.com', 'phone_number': '09131234567',
                                                'username':'admin', 'password':'1234', 'password2':'1234'})
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)

    def test_unmatched_password(self):
        srz_data = UserRegisterSerializer(
            data={'staff_id': '1271677601', 'email': 'deli@gmail.com', 'phone_number': '09131234567',
                  'username': 'delaram', 'password': 'del_pass', 'password2': 'del_pass2'})
        self.assertFalse(srz_data.is_valid())
        self.assertEqual(len(srz_data.errors), 1)