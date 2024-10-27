from django.test import TestCase
from .models import CustomUser, Profile
from .factories import CustomUserFactory, ProfileFactory

class CustomUserTests(TestCase):
    """
    Test cases for CustomUser model.
    """
    def setUp(self):
        """
        Set up test environment.
        """
        self.user = CustomUserFactory()

    def test_create_user(self):
        """
        Test creating a new user.
        """
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_admin)
        self.assertFalse(self.user.is_superuser)

    def test_user_str(self):
        """
        Test the __str__ method.
        """
        self.assertEqual(str(self.user), self.user.email)

    def test_get_full_name(self):
        """
        Test the get_full_name method.
        """
        self.assertEqual(self.user.get_full_name(), f"{self.user.first_name} {self.user.last_name}")

    def test_get_short_name(self):
        """
        Test the get_short_name method.
        """
        self.assertEqual(self.user.get_short_name(), self.user.first_name)

    def test_has_perm(self):
        """
        Test the has_perm method.
        """
        self.assertTrue(self.user.has_perm(None))

    def test_has_module_perms(self):
        """
        Test the has_module_perms method.
        """
        self.assertTrue(self.user.has_module_perms(None))

    def test_is_admin(self):
        """
        Test the is_admin property.
        """
        self.assertFalse(self.user.is_admin)

class ProfileTests(TestCase):
    """
    Test cases for Profile model.
    """
    def setUp(self):
        """
        Set up test environment.
        """
        self.profile = ProfileFactory()

    def test_profile_creation(self):
        """
        Test that a profile is created for a new user.
        """
        self.assertTrue(isinstance(self.profile, Profile))
        self.assertTrue(isinstance(self.profile.user, CustomUser))

    def test_profile_str(self):
        """
        Test the string representation of the profile.
        """
        self.assertEqual(str(self.profile), f"{self.profile.user.username}'s profile")

    def test_get_profile_image_url(self):
        """
        Test the profile image URL method.
        """
        self.assertEqual(self.profile.get_profile_image_url(), '/static/images/default_profile.png')

    def test_get_age(self):
        """
        Test the get_age method.
        """
        self.assertIsNone(self.profile.get_age())

    