from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError

from Blogs.models import Post, Category, HashTag, PostImage


class BlogTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            email="test-user-email@gmail.com",
            user_name='test-user-username',
            password='test1234pass'
        )
        self.category = Category(name="category test 1")
        self.category.save()

        self.pending_post = Post(
            title='title-test-1',
            context='title-test-1',
            author=self.user,
        )

        self.pending_post.save()
        self.pending_post.category.add(self.category)
        self.pending_post.save()

    def test_str_method(self):
        self.assertEquals(str(self.pending_post), self.pending_post.title)

    def test_fields_post_model(self):
        self.assertEquals(self.pending_post.category.all()[0], self.category)
        self.assertEquals(self.pending_post.status, 'NULL')

    def test_the_author_of_the_post(self):
        self.assertEquals(self.pending_post.author.email, self.user.email)


class CategoryTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name="category test 1")

    def test_str_method(self):
        self.assertEquals(str(self.category), self.category.name)

    def test_adding_existing_name(self):
        with self.assertRaises(IntegrityError) as context:
            Category.objects.create(name=self.category.name)

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))


class HashTagTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            email="test-user-email@gmail.com",
            user_name='test-user-username',
            password='test1234pass'
        )

        self.pending_post = Post(
            title='title-test-1',
            context='title-test-1',
            author=self.user,
        )

        self.pending_post.save()
        self.hash_tag = HashTag(name="hash-tag test 1", post=self.pending_post)
        self.hash_tag.save()

    def test_str_method(self):
        self.assertEquals(str(self.hash_tag), self.hash_tag.name)

    def test_fields_hash_tag_model(self):
        self.assertEquals(self.hash_tag.post, self.pending_post)


class PostImageTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            email="test-user-email@gmail.com",
            user_name='test-user-username',
            password='test1234pass'
        )

        self.pending_post = Post(
            title='title-test-1',
            context='title-test-1',
            author=self.user,
        )

        self.pending_post.save()
        self.post_image = PostImage(name="post_image test 1", post=self.pending_post)
        self.post_image.save()

    def test_str_method(self):
        self.assertEquals(str(self.post_image), self.pending_post.title)

    def test_fields_post_image_model(self):
        self.assertEquals(self.post_image.post, self.pending_post)
