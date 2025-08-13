import datetime
from datetime import datetime, timezone
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth import get_user


from django.test.client import Client
from django.contrib.auth.hashers import check_password
from django.contrib.messages import get_messages
from accounts.models import Dashboard, PendingUser, Token
from django.contrib.messages.storage.base import Message

from conftest import client


User = get_user_model()  # Ensure that the User model is imported correctly

pytestmark = (
    pytest.mark.django_db
)  # Ensure that all tests run with a database transaction


# Test for registering a new user
def test_register_user(client: Client):
    url = reverse("register")
    data = {"password": "testuser", "email": "testuser@example.com"}
    response = client.post(url, data)
    assert response.status_code == 200
    pending_user = PendingUser.objects.filter(email=data["email"]).first()

    assert pending_user
    assert check_password(data["password"], pending_user.password)
    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "success"
    # Assuming the success message is set in the view
    assert "verification code sent to" in str(messages[0]).lower()


# Test for registering a user with an existing email
def test_register_user_duplicate_email(client: Client, user_instance):
    url = reverse("register")
    data = {"password": "testuser", "email": user_instance.email}  # already exists
    response = client.post(url, data)

    assert response.status_code == 302  # Redirect to register page
    # Check if the user is redirected to the register page
    assert response.url == reverse("register")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "error"
    assert "email exists" in messages[0].message.lower()


# Test for verify account with valid code


def test_verify_account_valid_code(client: Client):
    pending_user = PendingUser.objects.create(
        email="abc@gmail.com", verification_code="123456", password="testpassword"
    )
    url = reverse("verify_account")

    data = {"email": pending_user.email, "code": pending_user.verification_code}
    response = client.post(url, data)
    assert response.status_code == 302  # for redirection
    assert response.url == reverse(
        "dashboard"
    )  # Assuming the user is redirected to login after verification
    user = get_user(response.wsgi_request)
    assert user.is_authenticated


# Test for verify account with invalid code
def test_verify_account_invalid_code():
    client = Client()
    pending_user = PendingUser.objects.create(
        email="abc@gmail.com", verification_code="123456", password="testpassword"
    )

    url = reverse("verify_account")
    data = {"email": pending_user.email, "code": "wrongcode"}  # Invalid code
    response = client.post(url, data)
    assert response.status_code == 400  # Assuming the view returns 200 for invalid code
    assert User.objects.count() == 0  # No user should be created


# Test for login with valid credentials


def test_login_valid_credentials(client: Client, user_instance):
    url = reverse("login")

    data = {
        "email": user_instance.email,
        "password": "testpassword123",  # Plaintext password
    }
    response = client.post(url, data)
    assert response.status_code == 302  # Redirect after login
    assert response.url == reverse("dashboard")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].tags == "success"
    assert "you are now logged in" in messages[0].message.lower()


def test_login_invalid_credentials(client: Client, user_instance):
    url = reverse("login")
    data = {"email": user_instance.email, "password": "randominvalidpass"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("login")

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "error"
    assert "invalid" in str(messages[0]).lower()


# Dashboard Testing


# Create dashboard
def test_dashboard_created_for_authenticated_users(client, user_instance):
    """
    Ensure that when a user is created, the post_save signal creates a Dashboard
    and that the authenticated user can access it.
    """
    # The signal should already have created the dashboard
    dashboard = Dashboard.objects.filter(user=user_instance).first()
    assert dashboard is not None, "Dashboard was not created for this user."
    assert dashboard.user == user_instance

    # Log in
    client.force_login(user_instance)
    url = reverse("dashboard")  # replace with your actual dashboard URL name
    response = client.get(url)

    assert response.status_code == 200
    assert str(user_instance.email) in response.content.decode()


# Update dashboard
def test_user_can_update_dashboard(client, user_instance, dashboard_update_data):
    client.force_login(user_instance)

    url = reverse("dashboard")
    response = client.post(url, dashboard_update_data)
    assert response.status_code == 302  # redirect after update

    dashboard = Dashboard.objects.get(user=user_instance)
    assert dashboard.country == "NG"
    assert dashboard.city == "Lagos"


# Delete account/Dashboard
def test_user_can_delete_account_from_dashboard(
    client, user_instance, django_user_model
):
    client.force_login(user_instance)

    url = reverse("delete_dashboard")  # match your view name
    response = client.post(url, {"confirm": "yes"})  # assuming your form has this
    assert response.status_code == 302  # redirect after deletion

    # User should be gone
    assert not django_user_model.objects.filter(id=user_instance.id).exists()


# Can change password from dashboard
def test_user_can_change_password_from_dashboard(client, user_instance):
    # Login using fixture-provided user
    client.force_login(user_instance)

    url = reverse("change_password")
    data = {
        "old_password": "testpassword123",  # must match password in your fixture
        "new_password1": "newsecurepass456",
        "new_password2": "newsecurepass456",
    }

    response = client.post(url, data, follow=True)

    # Redirect or reload page after change
    assert response.status_code == 200
    messages = list(response.context["messages"])
    assert any("password" in str(m).lower() for m in messages)

    # Confirm password was updated
    client.logout()
    assert client.login(email=user_instance.email, password="newsecurepass456") is True


# =======Password testing======
# Test   test_initiate_password_reset_using_registered_email
def test_initiate_password_reset_using_registered_email(client: Client, user_instance):
    url = reverse("reset_password_via_email")
    data = {"email": user_instance.email}
    response = client.post(url, data)
    assert response.status_code == 302
    assert Token.objects.get(
        user__email=data["email"], token_type=Token.TokenType.PASSWORD_RESET
    )

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "success"
    assert str(messages[0]) == "Reset link sent to your email"


# test_initiate_password_reset_using_unregistered_email
def test_initiate_password_reset_using_unregistered_email(client: Client):
    url = reverse("reset_password_via_email")
    data = {"email": "notregistered@gmail.com"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert not Token.objects.filter(
        user__email=data["email"], token_type=Token.TokenType.PASSWORD_RESET
    ).first()

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "error"
    assert str(messages[0]) == "Email not found"


# test_set_new_password_using_valid_reset_token
def test_set_new_password_using_valid_reset_token(client: Client, user_instance):
    url = reverse("set_new_password")
    reset_token = Token.objects.create(
        user=user_instance,
        token_type=Token.TokenType.PASSWORD_RESET,
        token="abcd",
        created_at=datetime.now(timezone.utc),
    )

    data = {
        "password1": "12345",
        "password2": "12345",
        "email": user_instance.email,
        "token": reset_token.token,
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("login")
    assert Token.objects.count() == 0

    user_instance.refresh_from_db()
    assert user_instance.check_password(data["password1"])

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "success"
    assert str(messages[0]) == "Password changed."


# test_set_new_password_using_valid_reset_token
def test_set_new_password_using_invalid_reset_token(client: Client, user_instance):
    url = reverse("set_new_password")
    Token.objects.create(
        user=user_instance,
        token_type=Token.TokenType.PASSWORD_RESET,
        token="abcd",
        created_at=datetime.now(timezone.utc),
    )

    data = {
        "password1": "12345",
        "password2": "12345",
        "email": user_instance.email,
        "token": "Fakeinvalidtoken",
    }

    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse("reset_password_via_email")
    assert Token.objects.count() == 1

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].level_tag == "error"
    assert str(messages[0]) == "Expired or Invalid reset link"
