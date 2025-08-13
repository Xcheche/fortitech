from django.contrib import admin
from .models import Post, Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )  # Replace 'name' with the actual field(s) in your Category model
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "created_at",
        "updated_at",
        "status",
    )  # Ensure these fields exist in your Post model
    prepopulated_fields = {"slug": ("title",)}
    list_filter = (
        "status",
        "publish",
        "author",
        "category",
    )  # Add any other fields you want to filter by
    search_fields = ("title", "body")  # Fields to search in the admin interface
    date_hierarchy = "publish"  # Allows filtering by date in the admin interface
    ordering = ("-publish",)  # Default ordering of posts in the admin interface
    fieldsets = (
        (
            None,
            {"fields": ("title", "slug", "author", "category", "post_image", "body")},
        ),
        ("Publication Info", {"fields": ("status", "publish")}),
    )
    list_editable = (
        "status",
    )  # Allows inline editing of the status field in the list view
    actions = ["make_published", "make_draft"]  # Custom actions for bulk editing

    def make_published(self, _, queryset):
        queryset.update(status=Post.Status.PUBLISHED)

    def make_draft(self, _, queryset):
        queryset.update(status=Post.Status.DRAFT)

    make_published.short_description = "Mark selected posts as published"
    make_draft.short_description = "Mark selected posts as draft"


admin.site.register(Post, PostAdmin)
