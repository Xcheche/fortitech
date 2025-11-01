from django.conf import settings
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from blog.forms import CommentForm

from blog.models import Category, Comment, Post
from django.core.paginator import Paginator
from django.views.generic import ListView
from django.db.models import F
from django.contrib import messages
from django.http import JsonResponse

from common.tasks import send_email
from .forms import PostForm, SharePostForm  
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.views.generic import (UpdateView, DeleteView)
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from  django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
#====================================Home============================
class HomeView(ListView):
    """View to display the home page with a list of blog posts."""
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        return Post.published.all().order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["popular_posts"] = Post.published.order_by("-views")[:5]
        return context


#====================================== Category view=====================================
# This view will filter posts by the selected category
def posts_by_category(request, slug):
    """View to display posts filtered by category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category)

    paginator = Paginator(posts, 2)  # same paginate_by as HomeView
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)  # posts will have has_next, etc.
    return render(
        request, "blog/index.html", {"category_selected": category, "posts": posts}
    )




#================================== Post detail view========================================
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
    session_key = f"viewed_post_{post.pk}"
    if not request.session.get(session_key, False):
        Post.objects.filter(pk=post.pk).update(views=F("views") + 1)
        request.session[session_key] = True
        post.refresh_from_db(fields=["views"])

    # get reply target if exists
    reply_to = None
    reply_id = request.GET.get("reply_to")
    if reply_id:
        reply_to = Comment.objects.filter(id=reply_id, post=post).first()
        #TODO: Send email notification to comment author about reply

    # handle form
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            parent_id = request.POST.get("parent_id")
            comment.parent = (
                Comment.objects.filter(id=parent_id).first() if parent_id else None
            )
            comment.save()
            #TODO: Send email notification to post author about new comment
            messages.success(request, "Your comment has been added successfully.")
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


# Create Post

#================================= Create Post================================================
def  create_post(request):
    """View to create a new blog post."""
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to DB yet
            post.author = request.user      # Assign the current logged-in user
            post.save()                     # Now save to DB
            messages.success(request, 'Post created successfully!')
            return redirect('home')  # Redirect to home or post detail page
        
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blog/post.html', context)


    return redirect(request, 'blog/post.html')
  


#========================= Edit Post================================
class EditPostView(LoginRequiredMixin,UpdateView):
    """View to edit an existing blog post."""
    model = Post
    template_name = "blog/post.html"
    fields = ['title', 'body', 'category', 'post_image']  # Fields to be edited
    context_object_name = 'post'

    # Only allow the author to edit the post
    def form_valid(self, form): # Django cbv view without form dosent require save=false
        form.instance.author = self.request.user  # Set the author to the current logged in user
         # Add success message
        messages.success(self.request, "Your post has been successfully updated!")

        return super().form_valid(form)
    # Redirect to the post detail page after successful edit   
    def get_success_url(self):
        return self.object.get_absolute_url()  # Use the post's absolute URL (the detail page URL)
    # Ensure only the author can edit the post
    def test_func(self): # Check if the current user is the author of the post
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    
     



#====================================== Delete Post================================================
class DeleteView(DeleteView):
    """View to delete an existing blog post."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("home")
      # Redirect to home page after deletion


#============Share Post=========================
# Share post
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = SharePostForm(request.POST)
        if form.is_valid():
            # Process the form data
            cd = form.cleaned_data
            # Get absolute or canonical URL of the post
            post_url = request.build_absolute_uri(post.get_absolute_url())
            # Send the email
            # Note: Ensure you have configured your email settings in settings.py
            subject = f"{cd['name']} ({cd['email']}) recommends you read {post.title}"
            # message = (
            #     f"Read {post.title} at {post_url}\n\n"
            #     f"{cd['name']}'s comments: {cd['comments']}"
            # )
            # send_mail(
            #     subject=subject,
            #     message=message,
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     recipient_list=[cd["to"]],
            # )
            # sent = True
            #--switched to use common task send_email function with html template
            # Prepare email context
            context = {
                "post": post,
                "post_url": post_url,
                "name": cd["name"],
                "email": cd["email"],
                "comments": cd["comments"],
            }

            send_email(
                subject=subject,
                email_to=[cd["to"]],
                html_template="emails/share_post.html",
                context=context,
            )
            sent = True
            messages.success(request, "Post shared successfully!")
            return redirect(post.get_absolute_url())
    else:
        form = SharePostForm()
    context = {
        "form": form,
        "post": post,
        "sent": sent,
    }
    return render(request, "blog/share.html", context=context)
 
#=======================================All posts by a specific user=========================================
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, email=self.kwargs.get('email'))
        return Post.objects.filter(author=user).order_by('-created_at')





#======================== Search View========================================
#Use this if not using Q objects and want to return a result template and lopp through results 
#or return to index.html with results context and loop through results
# def search(request):
#     query = request.GET.get('q')
#     results = []

#     if query:
#         results = (
#             Post.published.filter(title__icontains=query) |
#             Post.published.filter(body__icontains=query) |
#             Post.published.filter(category__name__icontains=query)
#         ).distinct()

#     context = {
#         'results': results,
#         'query': query,
#     }
#     return render(request, 'blog/index.html', context)


#======================== Search View========================================
def search(request):
    import time  # noqa: F811

    time.sleep(1.5)
    query = request.GET.get('q')
    posts = Post.published.all()  # start with all posts

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    context = {
        'posts': posts,
        'query': query,
    }
    if not posts.exists():
        context["message"] = "No posts found."
    return render(request, 'blog/index.html', context)



#================================ Like a post and toggle on/off=========================================
@login_required


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({"liked": liked, "total_likes": post.total_likes()})