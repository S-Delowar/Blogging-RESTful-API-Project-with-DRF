from django.test import TestCase
from django.contrib.auth import get_user_model

from blog.models import Post


# Tests for Post Model
class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@mail.com",
            password="testpass"
        )
        
        cls.post = Post.objects.create(
            author = cls.user,
            title = "A Good Title",
            content = "Nice Body Content"
        )
        
    # post creation test
    def test_post_creation(self):
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.title, "A Good Title")
        self.assertEqual(self.post.content, "Nice Body Content")
        self.assertEqual(str(self.post), "A Good Title")