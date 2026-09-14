from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import PaymentFilter
from .models import Payment, User
from materials.serializers import PaymentSerializer
from .serializers import UserRegistrationSerializer, UserSerializer


class PaymentListView(ListAPIView):
    """Список платежей."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]

    filterset_class = PaymentFilter

    ordering_fields = ["payment_date"]
    ordering = ["-payment_date"]

class UserViewSet(viewsets.ModelViewSet):
    """CRUD пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class RegistrationView(generics.CreateAPIView):
    """Регистрация пользователя."""

    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

