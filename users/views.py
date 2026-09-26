from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course
from materials.serializers import PaymentSerializer

from .filters import PaymentFilter
from .models import Payment, Subscription, User
from .serializers import (
    PaymentCreateResponseSerializer,
    PaymentCreateSerializer,
    SubscriptionResponseSerializer,
    SubscriptionSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)
from .services.stripe_service import (
    create_checkout_session,
    create_stripe_price,
    create_stripe_product,
)


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


@extend_schema(
    summary="Добавление или удаление подписки",
    description=(
        "Добавляет подписку пользователя на курс "
        "или удаляет существующую подписку."
    ),
    request=SubscriptionSerializer,
    responses={
        200: SubscriptionResponseSerializer,
        401: OpenApiResponse(
            description="Пользователь не авторизован.",
        ),
        404: OpenApiResponse(
            description="Курс не найден.",
        ),
    },
)
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


@extend_schema(
    summary="Создание платежа через Stripe",
    description=(
        "Создает платеж для выбранного курса через Stripe "
        "и возвращает ссылку на страницу оплаты."
    ),
    request=PaymentCreateSerializer,
    responses={
        201: PaymentCreateResponseSerializer,
        401: OpenApiResponse(
            description="Пользователь не авторизован.",
        ),
        404: OpenApiResponse(
            description="Курс не найден.",
        ),
    },
)
class CreatePaymentView(APIView):
    """Создание платежа через Stripe."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course")

        course = get_object_or_404(
            Course,
            id=course_id,
        )

        product = create_stripe_product(course)

        price = create_stripe_price(
            course,
            product.id,
        )

        session = create_checkout_session(price.id)

        payment = Payment.objects.create(
            user=request.user,
            course=course,
            amount=course.price,
            payment_method="transfer",
        )

        return Response(
            {
                "payment_id": payment.id,
                "payment_url": session.url,
                "session_id": session.id,
            },
            status=status.HTTP_201_CREATED,
        )