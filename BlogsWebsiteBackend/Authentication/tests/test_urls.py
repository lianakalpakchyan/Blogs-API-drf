from django.urls import reverse, resolve
from django.test import SimpleTestCase

from Authentication.views import RegisterView, LoginAPIView, LogoutAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


class UrlsTest(SimpleTestCase):
    def test_register(self):
        path = resolve('/auth/register/')
        self.assertEquals(path.func.cls, RegisterView)
        self.assertNotEquals(path.func.cls, LoginAPIView)

    def test_login(self):
        path = resolve('/auth/login/')
        self.assertEquals(path.func.cls, LoginAPIView)
        self.assertNotEquals(path.func.cls, LogoutAPIView)

    def test_logout(self):
        path = resolve('/auth/logout/')
        self.assertEquals(path.func.cls, LogoutAPIView)
        self.assertNotEquals(path.func.cls, TokenRefreshView)

    def test_token_refresh(self):
        path = resolve('/auth/token/refresh/')
        self.assertEquals(path.func.cls, TokenRefreshView)
        self.assertNotEquals(path.func.cls, RegisterView)
