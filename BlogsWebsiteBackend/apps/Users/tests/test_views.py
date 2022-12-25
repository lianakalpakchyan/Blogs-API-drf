from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework.test import APITestCase
from rest_framework import status

from apps.Users.serializers import ProfileSerializer


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

    def test_get_profile(self):
        path = '/users/profile/'
        response = self.client.get(path)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user['access']}"
        )
        response = self.client.get(path)
        serializer = ProfileSerializer(self.user)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(dict(response.data['results'][0]), serializer.data)
