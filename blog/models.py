from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.urls import reverse
from common.models import BaseModel
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


#============================ Custom manager to filter published posts=======================
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


#==================================== Category==========================================
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def get_absolute_url(self):
        return reverse("posts_by_category", args=[self.slug])

    def __str__(self):
        return self.name


#================================== Post Model extending from base model abstract class========================================
class Post(BaseModel):
    """Model representing a blog post."""
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
    #----- Cloudinary field for image upload to cloudinary------
    post_image = CloudinaryField(
        "post_image",
        folder="cyberguard_blog_images/",
        blank=True,
        null=True,
        # This is the transformation for the image
        transformation={"width": 300, "height": 200, "crop": "fill"},
    )
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blog_post",
    )
    body = RichTextField(blank=False)

    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    views_count = models.PositiveIntegerField(default=0)

    #----------------- Metadata for the post--------------------
    class Meta:
        ordering = ["-publish"]
        verbose_name_plural = "Posts"
        indexes = [
            models.Index(fields=["-publish"]),
        ]
    #----------------- String representation of the post--------------------
    def __str__(self):
        return self.title
    





    #=========================== Get absolute url using args positional arguments or kwargs keyword arguments could be used==========
    
    def get_absolute_url(self):

        """
        Returns the canonical URL for the post based on its publish date and slug.
        Raises a ValueError if slug or publish date is missing.
        """
        if not self.slug:
            raise ValueError("Post slug is missing. Cannot build post detail URL.")
        if not self.publish:
            raise ValueError("Publish date is missing. Cannot build post detail URL.")

        return reverse(
            "post_detail",  # This should match the `name=` in your urls.py
            kwargs={
                "year": self.publish.year,
                "month": self.publish.month,
                "day": self.publish.day,
                "post": self.slug,  # slug must be non-empty!
            },
        )
   
    #=========================== Overriding the save method to auto-generate slug from title if not provided==========
    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug from title if not provided."""
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


#================================== Comment===========================
class Comment(BaseModel):
    """Model representing a comment on a blog post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    #----------------- Metadata for the comment--------------------
    class Meta:
        ordering = ["created_at"]
        verbose_name_plural = "Comments"
    #----------------- String representation of the comment--------------------  
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
