from django.urls import reverse
import pytest
from rest_framework import status


@pytest.mark.django_db
class TestMeView:
    def test_returns_authenticated_user_profile(self, api_client, active_user):
        api_client.force_authenticate(user=active_user)
        response = api_client.get(reverse("auth-me"))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == active_user.email
        assert response.data["role"] == active_user.role
        assert response.data["is_active"] is True
        assert "id" in response.data
        assert "date_joined" in response.data

    def test_unauthenticated_request_is_rejected(self, api_client):
        response = api_client.get(reverse("auth-me"))
        assert response.status_code in (
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        )
