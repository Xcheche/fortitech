from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from blog.forms import CommentForm
from blog.models import Category, Comment, Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import F


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
     
        context["popular_posts"] = Post.published.order_by("-views_count")[:5]
        return context


# Category view
# This view will filter posts by the selected category
def posts_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category)

    paginator = Paginator(posts, 2)  # same paginate_by as HomeView
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)  # posts will have has_next, etc.
    return render(
        request, "blog/index.html", {"category_selected": category, "posts": posts}
    )


# Post detail view
# This view will display the details of a single post, including comments and a form to add

@login_required
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )

    # increase views
    Post.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
    post.refresh_from_db()

    # get reply target if exists
    reply_to = None
    reply_id = request.GET.get("reply_to")
    if reply_id:
        reply_to = Comment.objects.filter(id=reply_id, post=post).first()

    # handle form
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get("parent_id")
            comment.parent = Comment.objects.filter(id=parent_id).first() if parent_id else None
            comment.save()
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    comments = post.comments.filter(parent__isnull=True)

    context = {
        "post": post,
        "comments": comments,
        "form": form,
        "reply_to": reply_to,
    }
    return render(request, "blog/post_detail.html", context)
