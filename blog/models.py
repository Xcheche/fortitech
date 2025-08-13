from django.utils import timezone
from django.db import models

from django.conf import settings
from django.urls import reverse
from common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


# Custom manager to filter published posts
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Category
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse("posts_by_category", args=[self.slug])

    def __str__(self):
        return self.name


# Model for blog posts
# Inherits from BaseModel which has created_at and updated_at fields
# The Post model represents a blog post with fields for title, slug, author, body,
class Post(BaseModel):
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="post_category"
    )
    post_image = models.ImageField(
        upload_to="post_images/%Y/%m/%d/", blank=True, null=True
    )
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_post",
    )
    body = models.TextField()

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )

    # Metadata for the post
    class Meta:
        ordering = ["-publish"]
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
    
 
    # Get absolute url using args positional arguments or kwargs keyword arguments could be used
    # Canonical URL for the post
    def get_absolute_url(self):
        return reverse(
            "post_detail",
            kwargs={
                "post": self.slug,
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
            },
        )
