from django.urls import reverse, resolve
from django.test import SimpleTestCase

from Blogs.views import PostViewset
from Users.views import ProfileViewset


class UrlsTest(SimpleTestCase):
    def test_user_profile(self):
        path = resolve('/users/profile/')
        self.assertEquals(path.func.cls, ProfileViewset)
        self.assertNotEquals(path.func.cls, PostViewset)
