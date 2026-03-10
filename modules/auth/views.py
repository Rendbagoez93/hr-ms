from typing import ClassVar

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UserProfileSerializer


# --- SimpleJWT integration point -------------------------------------------
# When djangorestframework-simplejwt is installed:
#
#   from rest_framework_simplejwt.tokens import RefreshToken
#
#   def _token_pair(user):
#       refresh = RefreshToken.for_user(user)
#       return {"refresh": str(refresh), "access": str(refresh.access_token)}
#
# Replace the stub below with the real implementation and update
# DEFAULT_AUTHENTICATION_CLASSES in settings to use JWTAuthentication.
# ---------------------------------------------------------------------------


def _token_pair(_user) -> dict:
    """Placeholder — swap for SimpleJWT once the package is added."""
    return {}


class LoginView(APIView):
    permission_classes: ClassVar[list] = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                **_token_pair(user),
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, _request):
        # Blacklist the refresh token here once SimpleJWT is active.
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def get(self, request):
        return Response(UserProfileSerializer(request.user).data)
