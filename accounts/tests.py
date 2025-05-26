import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
def test_admin_can_create_user():
    admin = User.objects.create_user(username="admin", password="pass", role="admin")

    client = APIClient()
    response = client.post("/api/token/", {"username": "admin", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    data = {
        "username": "novo_usuario",
        "password": "senha123",
        "email": "novo@exemplo.com",
    }
    response = client.post("/api/accounts/users/", data)
    assert response.status_code == 201
    assert User.objects.filter(username="novo_usuario").exists()


@pytest.mark.django_db
def test_user_cannot_create_user():
    user = User.objects.create_user(username="user", password="pass", role="editor")

    client = APIClient()
    response = client.post("/api/token/", {"username": "user", "password": "pass"})
    assert response.status_code == 200
    token = response.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    data = {
        "username": "usuario_criado",
        "password": "senha123",
        "email": "nao_deve@criar.com",
    }
    response = client.post("/api/accounts/users/", data)
    assert response.status_code == 403
    assert not User.objects.filter(username="usuario_criado").exists()


@pytest.mark.django_db
def test_user_cannot_update_other_user():
    user = User.objects.create_user(username="user", password="pass")
    other = User.objects.create_user(username="other", password="pass")

    client = APIClient()
    response = client.post("/api/token/", {"username": "user", "password": "pass"})
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {"email": "hackeado@exemplo.com"}
    response = client.patch(f"/api/accounts/users/{other.id}/", data)
    assert response.status_code == 403
    other.refresh_from_db()
    assert other.email != "hackeado@exemplo.com"


@pytest.mark.django_db
def test_admin_can_update_any_user():
    admin = User.objects.create_user(username="admin", password="pass", role="admin")
    user = User.objects.create_user(
        username="user", password="pass", email="old@exemplo.com"
    )

    client = APIClient()
    response = client.post("/api/token/", {"username": "admin", "password": "pass"})
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    data = {"email": "atualizado@exemplo.com"}
    response = client.patch(f"/api/accounts/users/{user.id}/", data)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.email == "atualizado@exemplo.com"


@pytest.mark.django_db
def test_user_cannot_delete_other_user():
    user = User.objects.create_user(username="user", password="pass")
    other = User.objects.create_user(username="other", password="pass")

    client = APIClient()
    response = client.post("/api/token/", {"username": "user", "password": "pass"})
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.delete(f"/api/accounts/users/{other.id}/")
    assert response.status_code == 403
    assert User.objects.filter(id=other.id).exists()


@pytest.mark.django_db
def test_admin_can_delete_any_user():
    admin = User.objects.create_user(username="admin", password="pass", role="admin")
    user = User.objects.create_user(username="user", password="pass")

    client = APIClient()
    response = client.post("/api/token/", {"username": "admin", "password": "pass"})
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    response = client.delete(f"/api/accounts/users/{user.id}/")
    assert response.status_code == 204
    assert not User.objects.filter(id=user.id).exists()
