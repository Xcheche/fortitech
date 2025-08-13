from django.db.models import Count
from .models import Category, Post

# Gets all draft and published posts
# def categories_with_post_count(request):
#     categories = Category.objects.annotate(post_count=Count('post_category'))
#     return {'categories_with_post_count': categories}


# Get only published post instead of all posts
# This context processor will add categories with their post count to the context
from django.db.models import Count, Q


def categories_with_post_count(request):
    return {
        "categories_with_post_count": Category.objects.annotate(
            post_count=Count(
                "post_category", filter=Q(post_category__status=Post.Status.PUBLISHED)
            )
        )
    }
