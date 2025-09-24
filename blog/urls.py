from django.urls import path
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
    path("delete_post/<uuid:pk>/", views.DeleteView.as_view(), name="delete_post")
]
