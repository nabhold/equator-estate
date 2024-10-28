from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings


class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle creating user and superuser.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model extending AbstractBaseUser and PermissionsMixin."""

    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=150, unique=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=30, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    is_admin = models.BooleanField(_("admin status"), default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email

    def get_full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Returns the user's short name."""
        return self.first_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Profile(models.Model):
    """
    Profile model to store additional user information.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    profile_image = models.ImageField(
        _("profile image"), upload_to="profile_images/", blank=True, null=True
    )
    bio = models.TextField(_("bio"), blank=True, null=True)
    phone_number = models.CharField(
        _("phone number"), max_length=15, blank=True, null=True
    )
    website = models.URLField(_("website"), blank=True, null=True)
    address = models.TextField(_("address"), blank=True, null=True)
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}'s profile"

    def get_profile_image_url(self):
        """
        Returns the URL to the user's profile image or a default image.
        """
        if self.profile_image:
            return self.profile_image.url
        return "/static/images/default_profile.png"

    def get_age(self):
        """
        Calculates and returns the user's age based on their date of birth.
        """
        if self.date_of_birth:
            return timezone.now().year - self.date_of_birth.year
        return None

    def has_complete_profile(self):
        """
        Checks if the user's profile is complete.
        """
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.user.username,
        ]
        return all(required_fields)
