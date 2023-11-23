from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CustomLoginSerializer

# Create your views here.
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer

    def post(self, *args, **kwargs):
        serializer = self.get_serializer(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.get_token(user)

        response_data = self.get_response_data(token, user, *args, **kwargs)
        response = Response(response_data, status=self.get_response_status())
        if self.get_response_status() == 200:
            response.set_cookie(
                "jwt", token, httponly=True, secure=True
            )  # Configura tu cookie JWT según tus necesidades
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        response.delete_cookie('jwt')  # Elimina la cookie JWT al cerrar sesión
        return response