import django_filters


from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """Фильтр для платежей."""

    class Meta:
        model = Payment
        fields = [
            "course",
            "lesson",
            "payment_method",
        ]
