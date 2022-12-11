from django.contrib.auth import get_user_model
from django.test import TestCase


class ManagersTest(TestCase):
    def test_create_user_without_user_name(self):
        with self.assertRaises(TypeError):
            user = get_user_model().objects.create_user(
                first_name="test-user-first-name",
                last_name="test-user-last-name",
                email="test-user-email@gmail.com",
                password='test1234pass'
            )

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            email="test-user-email@gmail.com",
            user_name='test-user-username',
            password='test1234pass'
        )

        self.assertIsInstance(user, get_user_model())
        self.assertFalse(user.is_staff, user.is_superuser)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            first_name="test-superuser-first-name",
            last_name="test-superuser-last-name",
            email="test-superuser-email@gmail.com",
            user_name='test-superuser-username',
            password='test1234pass'
        )

        self.assertIsInstance(superuser, get_user_model())
        self.assertTrue(superuser.is_staff, superuser.is_superuser)

