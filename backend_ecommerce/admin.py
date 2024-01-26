from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published',)
    list_editable = ('is_published',)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item', 'stars', 'comment', 'comment_date']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'ordered', 'payment_id', 'get_items_display', 'payment_option_verbose',)
    search_fields = ('user__username',)

    def payment_id(self, obj):
        payment = obj.payment_set.first()
        checkout_details = CheckoutDetails.objects.get(order=obj)
        # отримати перший Payment об'єкт, якщо він існує
        if checkout_details.payment_option == "C":
            return f'Need to call the user back to confirm the order'
        if payment and payment.stripe_id:
                url = payment.get_stripe_url()
                html = f'<a href="{url}">{payment.stripe_id}</a>'
                return mark_safe(html)
        return ''

    payment_id.short_description = 'Payment ID'

    def get_items_display(self, obj):
        items = obj.items.all()
        return mark_safe('<br>'.join([f"{item.item.title} - {item.quantity}" for item in items]))

    get_items_display.short_description = "Items"

    def payment_option_verbose(self, obj):
        checkout_details = CheckoutDetails.objects.get(order=obj)
        return dict(CheckoutDetails.PAYMENT_CHOICES)[obj.checkout_details.payment_option]

    payment_option_verbose.short_description = "Payment Option"


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'quantity', 'ordered')
    ordering = ['user__username', ]
    search_fields = ('user__username',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Review, ReviewsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Category)
admin.site.register(CheckoutDetails)
