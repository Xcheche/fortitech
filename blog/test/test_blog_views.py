from importlib.resources import contents
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from blog.models import  Post
from blog.views import post_detail
from conftest import client
User = get_user_model()



# Mark all tests in this file as requiring the Django test database
pytestmark = (
    pytest.mark.django_db
)  


@pytest.mark.django_db
def test_authenticated_user_can_create_blog(client: client,
                                             user_instance,
                                             post_create):

    client.force_login(user_instance)

    create_blog_url = reverse('create_post')
    response = client.get(create_blog_url)
    assert response.status_code == 200
    content = str(response.content)
    assert "<form" in content   # ✅ confirm the page has a form to create blog



@pytest.mark.django_db
def test_authenticated_user_can_update_blog(client: client,
                                             user_instance,
                                             edit_post):

    client.force_login(user_instance)

    edit_blog_url = reverse('edit_post', args=[edit_post.id])
    response = client.get(edit_blog_url)
    assert response.status_code == 200
    content = str(response.content)
    assert "<form" in content   # ✅ confirm the page has a form to edit blog



@pytest.mark.django_db
def test_authenticated_user_can_delete_blog(client: client,
                                             user_instance,
                                             edit_post):

    client.force_login(user_instance)

    delete_blog_url = reverse('delete_post', args=[edit_post.id])
    response = client.post(delete_blog_url)
    assert response.status_code == 302  # Assuming a redirect after deletion

    # Verify the post is deleted
    with pytest.raises(Post.DoesNotExist):
        Post.objects.get(id=edit_post.id)
