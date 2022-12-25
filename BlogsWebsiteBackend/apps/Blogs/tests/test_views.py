from django.contrib.auth import get_user_model
from django.core.cache import cache

from rest_framework.test import APITestCase
from rest_framework import status

from apps.Blogs.models import Category


class PostViewsetTest(APITestCase):
    def setUp(self) -> None:
        cache.clear()

        self.non_admin_1 = get_user_model().objects.create_user(
            first_name="test-non-admin-1-first-name",
            last_name="test-non-admin-1-last-name",
            email="test-non-admin-1-email@gmail.com",
            user_name='test-non-admin-1-username',
            password='test1234pass'
        )

        self.non_admin_2 = get_user_model().objects.create_user(
            first_name="test-non-admin-2-first-name",
            last_name="test-non-admin-2-last-name",
            email="test-non-admin-2-email@gmail.com",
            user_name='test-non-admin-2-username',
            password='test1234pass'
        )

        self.moderator = get_user_model().objects.create_user(
            first_name="test-moderator-user-first-name",
            last_name="test-moderator-user-last-name",
            email="test-moderator-user-email@gmail.com",
            user_name='test-moderator-user-username',
            password='test1234pass',
            role='MODERATOR'
        )
        self.category = Category.objects.create(name="category test 1")

        self.post_valid_non_admin_1 = {
            "title": "title 1",
            "context": "context 1",
            "image": [
                {
                    "name": "https://images.unsplash.com/photo-1471879832106-c7ab9e0cee23?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxleHBsb3JlLWZlZWR8Mnx8fGVufDB8fHx8&w=1000&q=80"
                }
            ],
            "hash_tag": [
                {
                    "name": "hash tag 1"
                }
            ],
            "category_id": [
                1
            ]
        }

        self.put_valid_non_admin_1 = {
            "title": "title 2",
            "context": "context 2",
            "hash_tag": [
                {
                    "name": "hash tag 2"
                }
            ],
            "category_id": [
                1
            ]
        }

        self.non_admin_2_changes_not_self_post = {
            "title": "not my title",
            "context": "not my context",
        }

        self.put_moderator_approved = {
            "status": "APPROVED",
        }

        self.refresh_for_non_admin_1 = self.non_admin_1.tokens()
        self.refresh_for_non_admin_2 = self.non_admin_2.tokens()
        self.refresh_for_moderator = self.moderator.tokens()

        self.POSTS_PATH = '/blogs/posts/'

    def test_get_with_and_without_authentication(self):
        path = self.POSTS_PATH
        response = self.client.get(path)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )

        response = self.client.get(path)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['results'], [])

    def test_post_with_and_without_authentication(self):
        path = self.POSTS_PATH
        response = self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        response = self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_put_with_pending_post(self):
        path = self.POSTS_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )

        response = self.client.put(
            path=f'{path}1/',
            data=self.put_valid_non_admin_1,
        )

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_with_not_pending_post(self):
        path = self.POSTS_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_moderator['access']}"
        )
        self.client.put(
            path=f'{path}1/',
            data=self.put_moderator_approved,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        response = self.client.put(
            path=f'{path}1/',
            data=self.put_valid_non_admin_1,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_with_pending_post(self):
        path = self.POSTS_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )

        response = self.client.delete(
            path=f'{path}1/',
        )

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_with_not_pending_post(self):
        path = self.POSTS_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_moderator['access']}"
        )
        self.client.put(
            path=f'{path}1/',
            data=self.put_moderator_approved,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        response = self.client.delete(
            path=f'{path}1/',
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_admin_2_changes_not_self_post(self):
        path = self.POSTS_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_2['access']}"
        )
        response = self.client.put(
            path=f'{path}1/',
            data=self.non_admin_2_changes_not_self_post,
        )
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_non_admin_2_deletes_not_self_post(self):
        path = self.POSTS_PATH
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_1['access']}"
        )
        self.client.post(
            path=path,
            data=self.post_valid_non_admin_1,
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_non_admin_2['access']}"
        )
        response = self.client.delete(
            path=f'{path}1/',
        )
        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CategoryViewsetTest(APITestCase):
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

        self.category = Category.objects.create(name="category test 1")

        self.CATEGORIES_PATH = '/blogs/categories/'

    def test_get_with_and_without_authentication(self):
        path = self.CATEGORIES_PATH
        response = self.client.get(path)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user['access']}"
        )

        response = self.client.get(path)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(dict(response.data['results'][0]), {'id': 1, 'name': 'category test 1'})
