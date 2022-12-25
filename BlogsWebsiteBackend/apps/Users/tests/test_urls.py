from django.urls import resolve
from django.test import SimpleTestCase

from apps.Users.views import ProfileViewset


class UrlsTest(SimpleTestCase):
    def test_user_profile(self):
        path = resolve('/users/profile/')
        self.assertEquals(path.func.cls, ProfileViewset)
