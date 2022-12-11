from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework.test import APITestCase
from rest_framework import status


class ViewsTest(APITestCase):
    def setUp(self) -> None:
        cache.clear()

        self.user = get_user_model().objects.create_user(
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            email="test-user-email@gmail.com",
            user_name='test-user-username',
            password='test1234pass'
        )
        self.refresh_for_user = self.user.tokens()

        self.invalid_email = {
            "email": "test-user-email",
        }
        self.user_email = {
            "email": f"{self.user.email}",
        }
        self.new_user = {
            "email": "panda@gmail.com",
            "user_name": "panda",
            "first_name": "panda",
            "last_name": "panda",
            "password": "test1234pass"
        }

        self.REGISTER_PATH = '/auth/register/'
        self.LOGIN_PATH = '/auth/login/'
        self.LOGOUT_PATH = '/auth/logout/'

    # REGISTER START
    def test_register_with_invalid_email(self):
        path = self.REGISTER_PATH
        response = self.client.post(
            path=path,
            data=self.invalid_email,
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_existing_email(self):
        path = self.REGISTER_PATH
        response = self.client.post(
            path=path,
            data=self.user_email,
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_new_email(self):
        path = self.REGISTER_PATH
        response = self.client.post(
            path=path,
            data=self.new_user
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    # REGISTER END

    # LOGIN START
    def test_login_with_invalid_email(self):
        path = self.LOGIN_PATH
        response = self.client.post(
            path=path,
            data=self.invalid_email,
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_non_existing_email(self):
        path = self.LOGIN_PATH
        response = self.client.post(
            path=path,
            data={
                "email": "test-user-email_fake@gmail.com",
                "password": 'test1234pass'
            }
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_valid_email(self):
        path = self.LOGIN_PATH
        response = self.client.post(
            path=path,
            data={
                "email": "test-user-email@gmail.com",
                "password": 'test1234pass'
            }
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
    # LOGIN END

    # START LOGOUT
    def test_logout_with_valid_data(self):
        path = self.LOGOUT_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user['access']}"
        )
        response = self.client.post(
            path=path,
            data={
                "refresh": self.refresh_for_user['refresh']
            }
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_with_invalid_refresh(self):
        path = self.LOGOUT_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user['access']}"
        )
        response = self.client.post(
            path=path,
            data={
                "refresh": 'Invalid refresh!'
            }
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

