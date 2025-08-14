from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog.models import Category, Post
from django.core.paginator import Paginator 
from django.views.generic import ListView

# Create your views here.
class HomeView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 2
    
    def get_queryset(self):
        return Post.published.all().order_by("-created_at")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Home"
        context["breadcrumbs"] = [
            {"name": "Home", "url": None},  # Fixed: No URL for current page
        ]
        return context
# Category view
# This view will filter posts by the selected category
def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category)
    return render(
        request, "blog/index.html", {"category_selected": category, "posts": posts}
    )


# def detail(request):
#     context = {
#         "page_title": "Blog Detail",
#         "breadcrumbs": [
#             {"name": "Home", "url": "/"},  # The current page is 'Home'
#             {"name": "Blog", "url": "/blog"},  # Link to the blog index
#            # {"name": slug, "url": f"/blog/{slug}"},  # Current blog post
#         ],
#     }
#     return render(request, "blog/detail.html", context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    context = {
        "page_title": "Blog Detail",
        "breadcrumbs": [
            {"name": "Home", "url": "/"},  # The current page is 'Home'
            {"name": "Blog", "url": "/blog"},  # Link to the blog index
            # {"name": slug, "url": f"/blog/{slug}"},  # Current blog post
        ],
    }
    return render(request, "blog/post_detail.html", {"post": post})
