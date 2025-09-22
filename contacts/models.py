from django.db import models
from common.models import BaseModel

# Create your models here.


class Contact(BaseModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    message = models.TextField()
    purpose = models.CharField(
        max_length=100,
        choices=[
            ("inquiry", "Inquiry"),
            ("register_course", "Register Course"),
            ("other", "Other"),
        ],
        default="inquiry",
    )

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.name} {self.email}"
