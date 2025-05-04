from urllib import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from blog.models import Post


# Tests for Post Model
class PostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@mail.com", password="testpass"
        )
        self.post = Post.objects.create(
            title="A Good Title",
            content="Nice Body Content",
            author=self.user
        )

    # test for creating post
    def test_post_creation(self):
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(self.post.title, "A Good Title")
        self.assertEqual(self.post.content, "Nice Body Content")

    # test for model's return by __str__ 
    def test_post_str_method(self):
        self.assertEqual(str(self.post), "A Good Title")
    

# ===========================================
# Tests for Post API endpoints
class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            email="user1@mail.com", username="user1", password="test123"
        )
        self.user2 = get_user_model().objects.create_user(
            email="user2@mail.com", username="user2", password="test456"
        )
        
        # Sample Post
        self.post = Post.objects.create(
            title = "A Good Title",
            content = "Nice Body Content",
            author = self.user1
        )
        
        # Token for authentication
        refresh = RefreshToken.for_user(self.user1)
        self.token = str(refresh.access_token)
        self.user1_auth_header = f"Bearer {self.token}"
        
    # test for listing posts with pagination
    def test_list_posts(self):
        url = reverse("post-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data) # check pagination
    
    # test for post creation by authenticated user 
    def test_create_post_authenticated(self):
        data = {
            "title": "New Post", "content": "New Content"
        }
        url = reverse("post-list")
        # token authorization-
        self.client.credentials(HTTP_AUTHORIZATION=self.user1_auth_header)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], self.user1.username)
        
    # test for post creation by unauthenticated user
    def test_create_post_unauthenticated(self):
        data = {
            "title": "New Post", "content": "New Content"
        }
        url = reverse("post-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # test for updating post by the post author
    def test_update_own_post(self):
        url = reverse("post-detail", args=[self.post.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.user1_auth_header)
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")
    
    # test for updating other's post
    def test_update_other_post(self):
        post_2 = Post.objects.create(
            title="Post for User-2",
            content = "Content for User-2",
            author = self.user2
        )
        url = reverse("post-detail", args=[post_2.id])
        # login as user1-
        self.client.credentials(HTTP_AUTHORIZATION=self.user1_auth_header)
        # updating post of user2
        response = self.client.patch(url, {"title": "New Title"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    # test for delete post by author
    def test_delete_post_by_author(self):
        url = reverse("post-detail", args=[self.post.id])
        self.client.credentials(HTTP_AUTHORIZATION=self.user1_auth_header)
        # delete-
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())  