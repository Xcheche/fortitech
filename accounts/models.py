from datetime import datetime, timezone
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager
from common.models import BaseModel
from django_countries.fields import CountryField
from PIL import Image
from ckeditor.fields import RichTextField
from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField

# Create your models here.


class User(
    BaseModel, AbstractBaseUser, PermissionsMixin
):  # Inheriting the basemodel abstract class from common folder
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# Email verification
class PendingUser(
    BaseModel
):  # Inheriting the basemodel abstract class from common folder
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    verification_code = models.CharField(max_length=255)

    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60
        now = datetime.now(timezone.utc)

        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        if timediff > lifespan_in_seconds:
            return False
        return True

    def __str__(self):
        return self.email


# For reset


class Token(BaseModel):
    class TokenType(models.TextChoices):
        PASSWORD_RESET = ("PASSWORD_RESET", "PASSWORD_RESET")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=100, choices=TokenType.choices)

    def __str__(self):
        return f"{self.user}  {self.token}"

    # check if token is valid
    def is_valid(self) -> bool:
        lifespan_in_seconds = 20 * 60  # 20 mins
        now = datetime.now(timezone.utc)
        timediff = now - self.created_at
        timediff = timediff.total_seconds()
        if timediff > lifespan_in_seconds:
            return False
        return True

    # resetting the user password
    def reset_user_password(self, raw_password: str):
        self.user: User
        self.user.set_password(raw_password)
        self.user.save()


# User dashboard


class Dashboard(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="dashboard"
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    nick_name = models.CharField(max_length=10)

    address = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    city = models.CharField(max_length=30, blank=True, null=True)

    post_code = models.CharField(max_length=100, blank=True, null=True)

    # profile_picture = models.ImageField(
    #     upload_to="profile_pictures/%Y/%m/%d/",
    #     null=True,
    #     blank=True,
    # )
    profile_picture = CloudinaryField(
        "dashboard",
        folder="cyberguard_blog_profile_images/",
        null=True,
        blank=True,
        transformation={"width": 200, "height": 200, "crop": "fill"},
    )

    def __str__(self):
        return f"Dashboard for {self.user.email}"

    class Meta:
        verbose_name = "Dashboard"
        verbose_name_plural = "Dashboard"

    # Resizing profile_picture automatically
    # def save(self, *args, **kwargs):
    #     # Call the parent save method with all arguments
    #     super().save(*args, **kwargs)

    #     # Resize the profile_picture
    #     if self.profile_picture:
    #         img = Image.open(self.profile_picture.path)
    #         if img.height > 300 or img.width > 300:
    #             output_size = (300, 300)
    #             img.thumbnail(output_size)
    #             img.save(self.profile_picture.path)
    # Resizing profile_picture automatically
    def save(self, *args, **kwargs):
    # Call the parent save method with all arguments
     super().save(*args, **kwargs)

    # Commented out because CloudinaryField doesn't have .path
    # if self.profile_picture:
    #     img = Image.open(self.profile_picture.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.profile_picture.path)
