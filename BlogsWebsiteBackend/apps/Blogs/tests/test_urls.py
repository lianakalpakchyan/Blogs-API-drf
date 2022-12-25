from django.urls import resolve
from django.test import SimpleTestCase

from apps.Blogs.views import PostViewset, CategoryViewset


class UrlsTest(SimpleTestCase):
    def test_posts(self):
        path = resolve('/blogs/posts/')
        self.assertEquals(path.func.cls, PostViewset)

    def test_categories(self):
        path = resolve('/blogs/categories/')
        self.assertEquals(path.func.cls, CategoryViewset)
