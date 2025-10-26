from django.urls import path
from . import views


urlpatterns = [
    # path('',views.landing,name='landing'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/delete/", views.delete_dashboard, name="delete_dashboard"),
    path(
        "dashboard/change-password/",
        views.DashboardPasswordChangeView.as_view(),
        name="change_password",
    ),
    path("about/", views.about, name="about"),
    # Auth
    path("register/", views.register, name="register"),
    path("verify_account/", views.verify_account, name="verify_account"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout, name="logout"),
    path(
        "forgot-password/",
        views.send_password_reset_link,
        name="reset_password_via_email",
    ),
    path(
        "verify-password-reset-link",
        views.verify_password_reset_link,
        name="verify_password_reset_link",
    ),
    path(
        "set-new-password/",
        views.set_new_password_using_reset_link,
        name="set_new_password",
    ),
]
