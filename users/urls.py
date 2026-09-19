from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegistrationView, SubscriptionView, UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path("register/", RegistrationView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path(
        "subscription/",
        SubscriptionView.as_view(),
        name="subscription",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]
