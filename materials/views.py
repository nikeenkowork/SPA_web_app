from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from users.filters import PaymentFilter
from users.models import Payment
from users.permissions import IsModerator, IsOwner
from .paginators import CustomPagination

from .models import Course, Lesson
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
)


class CourseViewSet(viewsets.ModelViewSet):
    """CRUD курсов."""

    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Course.objects.none()

        if IsModerator().has_permission(self.request, self):
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [
                IsAuthenticated,
                IsModerator | IsOwner,
            ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    """Список и создание уроков."""

    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Lesson.objects.none()

        if IsModerator().has_permission(self.request, self):
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [
                IsAuthenticated,
                IsModerator | IsOwner,
            ]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Просмотр, изменение и удаление урока."""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsModerator | IsOwner,
    ]


class PaymentListView(generics.ListAPIView):
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
