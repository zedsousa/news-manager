import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import Plan, User, Vertical
from news.models import News

User = get_user_model()


@pytest.mark.django_db
def test_authenticated_user_can_list_news():
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()
    response = client.post(
        "/api/token/", {"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.get("/api/news/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated_user_cannot_list_news():
    client = APIClient()
    response = client.get("/api/news/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_author_can_create_news():
    user = User.objects.create_user(username="author", password="pass", role="editor")
    client = APIClient()
    response = client.post("/api/token/", {"username": "author", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    vertical, _ = Vertical.objects.get_or_create(name="power")
    data = {
        "title": "New Article",
        "subtitle": "Subtitulo teste",
        "content": "Some interesting content",
        "status": "draft",
        "vertical": vertical.id,
        "is_pro": False,
    }
    response = client.post("/api/news/", data, format="json")
    assert response.status_code == 201, f"{response.status_code} - {response.data}"
    assert response.data["author"] == user.username


@pytest.mark.django_db
def test_author_can_edit_own_news():
    user = User.objects.create_user(username="author", password="pass", role="editor")
    news = News.objects.create(title="Título", content="Conteúdo", author=user)
    client = APIClient()
    response = client.post("/api/token/", {"username": "author", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    data = {"title": "Updated title"}
    response = client.patch(f"/api/news/{news.id}/", data)
    assert response.status_code == 200
    news.refresh_from_db()
    assert news.title == "Updated title"


@pytest.mark.django_db
def test_admin_can_edit_any_news():
    author = User.objects.create_user(username="author", password="pass")
    admin = User.objects.create_user(username="admin", password="pass", role="admin")
    news = News.objects.create(title="Título", content="Conteúdo", author=author)
    client = APIClient()
    response = client.post("/api/token/", {"username": "admin", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.patch(f"/api/news/{news.id}/", {"title": "Admin updated"})
    assert response.status_code == 200


@pytest.mark.django_db
def test_non_author_cannot_delete_others_news():
    author = User.objects.create_user(username="author", password="pass")
    other_user = User.objects.create_user(username="other", password="pass")
    news = News.objects.create(title="Título", content="Conteúdo", author=author)
    client = APIClient()
    response = client.post("/api/token/", {"username": "other", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.delete(f"/api/news/{news.id}/")
    assert response.status_code == 404


@pytest.mark.django_db
def test_admin_can_delete_any_news():
    author = User.objects.create_user(username="author", password="pass")
    admin = User.objects.create_user(username="admin", password="pass", role="admin")
    news = News.objects.create(title="Título", content="Conteúdo", author=author)
    client = APIClient()
    response = client.post("/api/token/", {"username": "admin", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.delete(f"/api/news/{news.id}/")
    assert response.status_code == 204
