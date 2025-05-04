from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from accounts.models import CustomUser


# Tests for CustomUser Model
class CustomUserTests(TestCase):
    
    # test for creating user
    def test_create_user(self):
        user = get_user_model().objects.create_user(
            username="testuser", email="testuser@mail.com", password="testpass123"
        )  
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "testuser@mail.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    
    # test for creating superuser
    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            username="superuser", email="superuser@mail.com", password="super123"
        )
        self.assertEqual(user.username, "superuser")
        self.assertEqual(user.email, "superuser@mail.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        

# ====================================================

# Tests for "/api/register/" for registering new user
class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
       
        
    # test for register with all required fields
    def test_register_user(self):
        data = {
            "username": "testuser", "email":"test@mail.com", "password": "test12345"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.first().email, "test@mail.com")


    # test for register without all required fields
    def test_register_with_missing_fields(self):
        data = {
            "username": "user", "email": "", "password": ""
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    # test for register with an email that is already used
    def test_register_duplicate_email(self):
        CustomUser.objects.create_user(
            username="user", email="user@mail.com", password="userpass123"
        )
        data = {
            "username": "new_user",
            "email": "user@mail.com",
            "password": "newpass123"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)