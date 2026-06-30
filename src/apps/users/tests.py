from django.test import TestCase

from apps.users.models import User
from apps.users.models import Address


class UserAddressModelsTestCase(TestCase):
    def test_address_can_be_created_for_user(self):
        user = User.objects.create_user(
            email='customer@example.com',
            password='securepass123',
            first_name='Test',
        )
        address = Address.objects.create(
            user=user,
            street='123 Main Street',
            city='Tashkent',
            state='Tashkent',
            zip_code='100000',
            country='Uzbekistan',
            label='home',
            is_default=True,
        )

        self.assertEqual(address.user, user)
        self.assertTrue(address.is_default)
