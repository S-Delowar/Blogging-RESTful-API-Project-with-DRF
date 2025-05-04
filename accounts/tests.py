from django.test import TestCase
from django.contrib.auth import get_user_model


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