from unittest.mock import patch

import pytest
from rest_framework.exceptions import ValidationError

from modules.auth.serializers import LoginSerializer


@pytest.mark.django_db
class TestLoginSerializer:
    def test_valid_credentials(self, active_user, user_password):
        serializer = LoginSerializer(
            data={"email": active_user.email, "password": user_password}
        )
        assert serializer.is_valid()
        assert serializer.validated_data["user"] == active_user

    def test_invalid_credentials_raises(self, active_user):
        serializer = LoginSerializer(
            data={"email": active_user.email, "password": "wrong_password"}
        )
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        assert "Invalid credentials" in str(exc_info.value.detail)

    def test_inactive_user_raises(self, active_user):
        # Simulate a custom backend that returns an inactive user
        active_user.is_active = False
        with patch("modules.auth.serializers.authenticate", return_value=active_user):
            serializer = LoginSerializer(
                data={"email": active_user.email, "password": "any_password"}
            )
            with pytest.raises(ValidationError) as exc_info:
                serializer.is_valid(raise_exception=True)
        assert "inactive" in str(exc_info.value.detail).lower()
