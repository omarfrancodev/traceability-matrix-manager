from django.urls import include, path
from .views import CustomLoginView, CustomLogoutView

urlpatterns = [
    # path("", include("dj_rest_auth.urls")),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
