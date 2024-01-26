from django import template
from backend_ecommerce.models import *

register = template.Library()


@register.filter
def cart_item_count(user):
    count_items = 0
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        for order in qs:
            for item in order.items.all():
                count_items += item.quantity
        return count_items
