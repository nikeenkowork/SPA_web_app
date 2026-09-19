from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from materials.serializers import PaymentSerializer

from .filters import PaymentFilter
from .models import Payment, Subscription, User
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


class SubscriptionView(APIView):
    """Установка и удаление подписки на курс."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get("course")

        course_item = get_object_or_404(
            Course,
            id=course_id,
        )

        subscription = Subscription.objects.filter(
            user=user,
            course=course_item,
        )

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user,
                course=course_item,
            )
            message = "Подписка добавлена"

        return Response(
            {"message": message},
        )


