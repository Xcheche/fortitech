from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth import get_user_model

from accounts.forms import DashboardUpdateForm, UserUpdateForm
from .models import *

from django.utils.crypto import get_random_string  # Create your views here.
from django.contrib.auth.hashers import make_password
from django.contrib import auth
from datetime import datetime
from common.tasks import send_email
from datetime import datetime, timezone
from .decorators import redirect_autheticated_user

# Password change
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()


# def landing(request):
#     if request.user.is_authenticated:
#         return redirect('dashboard')
#     else:
#         return render(request, 'blog/index.html')

# ====Dashboard
# def dashboard(request):
#     if request.method == 'POST':
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         dashboard_form = DashboardUpdateForm(request.POST, request.FILES, instance=request.user.dashboard)
#         if user_form.is_valid() and dashboard_form.is_valid():
#             user_form.save()
#             dashboard_form.save()
#             messages.success(request, 'Your dashboard has been updated!')
#             return redirect('dashboard')
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         dashboard_form = DashboardUpdateForm(instance=request.user.dashboard)
#     context = {
#         "page_title": "Dashboard",
#         "breadcrumbs": [
#             {"name": "Home", "url": "/"},
#             {"name": "Dashboard", "url": "dashboard"},
#         ],
#         'user_form': user_form,
#         'dashboard_form': dashboard_form,
#     }


#     return render(request, 'accounts/dashboard.html', context)
# @login_required
def dashboard(request):
    dashboard_obj = request.user.dashboard  # from related_name

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        dashboard_form = DashboardUpdateForm(
            request.POST, request.FILES, instance=dashboard_obj
        )

        if user_form.is_valid() and dashboard_form.is_valid():
            user_form.save()
            dashboard_form.save()
            messages.success(request, "Dashboard updated successfully!")
            return redirect("dashboard")
        else:
            # Show exactly what went wrong
            print("User form errors:", user_form.errors)
            print("Dashboard form errors:", dashboard_form.errors)
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserUpdateForm(instance=request.user)
        dashboard_form = DashboardUpdateForm(instance=dashboard_obj)

    return render(
        request,
        "accounts/dashboard.html",
        {
            "page_title": "Dashboard",
            "breadcrumbs": [
                {"name": "Home", "url": "/"},
                {"name": "Dashboard", "url": "dashboard"},
            ],
            "user_form": user_form,
            "dashboard_form": dashboard_form,
        },
    )


# ====Delete Dashboard
# This view handles the deletion of the user's dashboard. It deletes the dashboard and redirects to the


def delete_dashboard(request):
    if request.method == "POST":
        # You can either delete just the dashboard, or delete the whole user
        request.user.delete()  # deletes user and dashboard because of cascade
        messages.success(request, "Your account has been deleted.")
        return redirect("home")  # or a goodbye page

    return render(
        request, "accounts/delete_dashboard.html", {"page_title": "Delete Account"}
    )


# =====Change Password
# This view handles the change of the user's password. It checks if the old password is correct
class DashboardPasswordChangeView(PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("dashboard")

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)


# ====== Register view with email verification
# This view handles the registration of a new user. It checks if the email already exists in the database.
# If the email is new, it creates a new PendingUser object with a verification code and sends a verification email.
@redirect_autheticated_user
def register(request: HttpRequest):
    context = {
        "page_title": "Register",
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Register", "url": "Register"},
        ],
    }

    if request.method == "POST":
        email: str = request.POST["email"]
        password: str = request.POST["password"]
        cleaned_email = email.lower()

        if User.objects.filter(email=cleaned_email).exists():
            messages.error(request, "Email exists on the platform")
            return redirect("register")

        else:
            verification_code = get_random_string(10)
            PendingUser.objects.update_or_create(
                email=cleaned_email,
                defaults={
                    "password": make_password(password),
                    "verification_code": verification_code,
                    "created_at": datetime.now(timezone.utc),
                },
            )
            # Sending email
            send_email(
                "Verify Your Account",
                [cleaned_email],
                "emails/email_verification_template.html",
                context={"code": verification_code},
            )
            messages.success(request, f"Verification code sent to {cleaned_email}")

            # Add 'email' to the existing context for the POST response
            context["email"] = cleaned_email

            return render(request, "accounts/verify_account.html", context=context)

    else:
        return render(request, "accounts/register.html", context=context)


# ======= Verify Account


def verify_account(request: HttpRequest):

    if request.method == "POST":
        code: str = request.POST["code"]
        email: str = request.POST["email"]
        pending_user: PendingUser = PendingUser.objects.filter(
            verification_code=code, email=email
        ).first()
        if pending_user and pending_user.is_valid():
            user = User.objects.create(
                email=pending_user.email, password=pending_user.password
            )
            pending_user.delete()
            auth.login(request, user)
            messages.success(request, "Account verified. You are now logged in")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid or expired verification code")
            return render(
                request, "accounts/verify_account.html", {"email": email}, status=400
            )


# ======= Login view
# This view handles the login of existing users. It checks if the email and password are correct.
# If the credentials are valid, it logs the user in and redirects them to the home page.


@redirect_autheticated_user
def login(request: HttpRequest):
    context = {
        "page_title": "Register",
        "breadcrumbs": [
            {"name": "Home", "url": "/"},
            {"name": "Login", "url": "Login"},
        ],
    }

    if request.method == "POST":
        email: str = request.POST["email"]
        password: str = request.POST["password"]
        user = auth.authenticate(request, email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")
            return redirect("login")

    else:
        return render(request, "accounts/login.html", context=context)


# ======= Logout view
def logout(request: HttpRequest):
    auth.logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


# ====password_reset
def send_password_reset_link(request: HttpRequest):
    if request.method == "POST":
        email: str = request.POST.get("email", "")
        user = get_user_model().objects.filter(email=email.lower()).first()

        if user:
            token, _ = Token.objects.update_or_create(
                user=user,
                token_type=Token.TokenType.PASSWORD_RESET,
                defaults={
                    "token": get_random_string(20),
                    "created_at": datetime.now(timezone.utc),
                },
            )
            # Sending email
            email_data = {"email": email.lower(), "token": token.token}
            send_email(
                "Your Password Reset Link",
                [email],
                "emails/password_reset_template.html",
                email_data,
            )
            messages.success(request, "Reset link sent to your email")
            return redirect("reset_password_via_email")

        else:
            messages.error(request, "Email not found")
            return redirect("reset_password_via_email")

    else:
        return render(request, "accounts/forgot_password.html")


# =======verify_password
def verify_password_reset_link(request: HttpRequest):
    email = request.GET.get("email")
    reset_token = request.GET.get("token")

    token: Token = Token.objects.filter(
        user__email=email, token=reset_token, token_type=Token.TokenType.PASSWORD_RESET
    ).first()

    if not token or not token.is_valid():
        messages.error(request, "Invalid or expired reset link.")
        return redirect("reset_password_via_email")

    return render(
        request,
        "accounts/set_new_password_using_reset_token.html",
        context={"email": email, "token": reset_token},
    )


# ===========set_new_password
def set_new_password_using_reset_link(request: HttpRequest):
    """Set a new password given the token sent to the user email"""

    if request.method == "POST":
        password1: str = request.POST.get("password1")
        password2: str = request.POST.get("password2")
        email: str = request.POST.get("email")
        reset_token = request.POST.get("token")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(
                request,
                "accounts/set_new_password_using_reset_token.html",
                {"email": email, "token": reset_token},
            )

        token: Token = Token.objects.filter(
            token=reset_token,
            token_type=Token.TokenType.PASSWORD_RESET,
            user__email=email,
        ).first()

        if not token or not token.is_valid():
            messages.error(request, "Expired or Invalid reset link")
            return redirect("reset_password_via_email")
        # resetting the user password and deleting the token
        token.reset_user_password(password1)
        token.delete()
        messages.success(request, "Password changed.")
        return redirect("login")
