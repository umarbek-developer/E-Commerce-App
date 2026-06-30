from django.contrib.auth import get_user_model
from django.test import TestCase

from .serializers import UserSerializer

User = get_user_model()


class UserSerializerTests(TestCase):
    def test_update_profile_name_and_phone(self):
        user = User.objects.create_user(
            email='user@example.com',
            password='StrongPassword123!',
            first_name='Old',
            last_name='Name',
            phone_number='123456789',
        )

        serializer = UserSerializer(
            instance=user,
            data={'name': 'New Person', 'phone': '998901234567'},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        user.refresh_from_db()
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'Person')
        self.assertEqual(user.phone_number, '998901234567')
