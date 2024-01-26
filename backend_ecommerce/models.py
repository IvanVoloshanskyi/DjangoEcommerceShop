from django.conf import settings
from django.db import models
from django.urls import reverse
from django_countries.fields import CountryField


class Item(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)  # На індивідуальній сторінці
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", null=True, blank=True)
    price = models.FloatField()
    is_published = models.BooleanField(null=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('item-page', kwargs={"item_id": self.id})  # Or -> args=[str(self.id)]

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            'item_id': self.id
        })


class Review(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, related_name='reviews')
    stars = models.IntegerField(choices=RATING_CHOICES, blank=False, null=False)
    comment = models.CharField(max_length=100)
    advantages = models.CharField(max_length=50)
    disadvantages = models.CharField(max_length=50)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ['-comment_date']


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-page', args=[str(self.id)])


class OrderItem(models.Model):  # Shopping cart
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item.title} ID-{self.item.id} - x{self.quantity}"

    def get_item_price(self):
        return self.quantity * self.item.price

    class Meta:
        verbose_name_plural = "Shopping Cart"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True, null=True)
    ordered_date = models.DateTimeField(null=True)
    ordered = models.BooleanField(default=False)
    checkout_details = models.ForeignKey("CheckoutDetails", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_item_price()
        return total


class CheckoutDetails(models.Model):
    PAYMENT_CHOICES = (('C', 'Cash'),
                       ('B', 'Bank Transfer'),)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=20)
    country = CountryField(multiple=False)
    payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=15)
    zip = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=255, blank=True)

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
