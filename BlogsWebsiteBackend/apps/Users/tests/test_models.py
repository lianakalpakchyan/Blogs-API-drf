from django.contrib.auth import get_user_model
from django.test import TestCase


class UserTest(TestCase):
    def setUp(self) -> None:
        self.non_admin = get_user_model().objects.create_user(
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            email="test-user-email@gmail.com",
            user_name='test-user-username',
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

        self.admin = get_user_model().objects.create_user(
            first_name="test-admin-user-first-name",
            last_name="test-admin-user-last-name",
            email="test-user-admin-email@gmail.com",
            user_name='test-admin-user-username',
            password='test1234pass',
            role='ADMIN'
        )

        self.superuser = get_user_model().objects.create_superuser(
            first_name="test-superuser-first-name",
            last_name="test-superuser-last-name",
            email="test-superuser-email@gmail.com",
            user_name='test-superuser-username',
            password='test1234pass'
        )

    def test_str_method(self):
        self.assertEquals(str(self.non_admin), self.non_admin.user_name)
        self.assertEquals(str(self.moderator), self.moderator.user_name)
        self.assertEquals(str(self.admin), self.admin.user_name)
        self.assertEquals(str(self.superuser), self.superuser.user_name)

    def test_is_staff(self):
        self.assertEquals(self.non_admin.is_staff, False)
        self.assertEquals(self.moderator.is_staff, True)
        self.assertEquals(self.admin.is_staff, True)
        self.assertEquals(self.superuser.is_staff, True)

    def test_post_permissions(self):
        perms = ['Blogs.add_post', 'Blogs.view_post', 'Blogs.change_post', 'Blogs.delete_post']
        for perm in perms:
            self.assertEquals(self.non_admin.has_perm(perm), False)

        for perm in perms:
            self.assertEquals(self.moderator.has_perm(perm), True)

        for perm in perms:
            self.assertEquals(self.admin.has_perm(perm), True)

        for perm in perms:
            self.assertEquals(self.superuser.has_perm(perm), True)
