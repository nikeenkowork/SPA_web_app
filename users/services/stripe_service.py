from decimal import Decimal

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    product = stripe.Product.create(
        name=course.name,
        description=course.description,
    )

    return product


def create_stripe_price(course, product_id):
    amount = int(Decimal(str(course.price)) * 100)

    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency="czk",
    )

    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url="http://localhost:8000/payment/success/",
        cancel_url="http://localhost:8000/payment/cancel/",
    )

    return session
