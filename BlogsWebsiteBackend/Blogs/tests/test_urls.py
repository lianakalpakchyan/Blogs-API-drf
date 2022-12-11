from django.urls import reverse, resolve
from django.test import SimpleTestCase

from Blogs.views import PostViewset, CategoryViewset


class UrlsTest(SimpleTestCase):
    def test_posts(self):
        path = resolve('/blogs/posts/')
        self.assertEquals(path.func.cls, PostViewset)
        self.assertNotEquals(path.func.cls, CategoryViewset)

    def test_categories(self):
        path = resolve('/blogs/categories/')
        self.assertEquals(path.func.cls, CategoryViewset)
        self.assertNotEquals(path.func.cls, PostViewset)

