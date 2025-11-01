from django.urls import path

from blog.feeds import LatestPostsFeed

#from blog.feeds import LatestPostsFeed
from . import views 


urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    #========= Create Post=============
    path("create_post/",views.create_post,name="create_post"),
    #========= Edit Post=============
    path("edit_post/<uuid:pk>/", views.EditPostView.as_view(), name="edit_post"),
    #=================================
    path("category/<slug:slug>/", views.posts_by_category, name="posts_by_category"),
    #=================================Post detail view======================================== 
    path(
        "detail/<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.post_detail,
        name="post_detail",
    ),
    #================================= Delete Post========================================
    path("delete_post/<uuid:pk>/", views.DeleteView.as_view(), name="delete_post"),
    path('user_posts/<str:email>/', views.UserPostListView.as_view(), name='user-posts'),


    #================================= Share Post========================================
    path("share/<uuid:post_id>/", views.share_post, name="share_post"),

    #============================ Feed=============================================
    path("feed/", LatestPostsFeed(), name="post_feed"),
    #=============Search=========================
    path("search/", views.search, name="post_search"),
    path("like/<uuid:pk>/", views.like_post, name="like_post"),
]

