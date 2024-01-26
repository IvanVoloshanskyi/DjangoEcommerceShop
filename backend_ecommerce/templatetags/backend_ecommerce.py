from django import template
from backend_ecommerce.models import *

register = template.Library()


@register.simple_tag()
def pls_category():
    return Category.objects.all()
