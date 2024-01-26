from django.urls import path
from backend_ecommerce.views import *

urlpatterns = [
    path('', HomePage.as_view(), name="homepage"),
    path('item/<int:item_id>', ItemPage.as_view(), name="item-page"),
    path('category/<int:category_id>', ItemCategory.as_view(), name="category-page"),
    path('item/<int:item_id>/reviews/', ItemReview, name="item-review"),
    path('item/<int:item_id>/descriprion', ItemDescription.as_view(), name="item-description"),

    # CART URLS
    path('add-to-cart/<int:item_id>', add_to_cart, name="add-to-cart"),
    path('remove-from-cart/<int:item_id>', remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<int:item_id>', remove_single_item_from_cart, name="remove-item-from-cart"),
    path('shopping-cart/', OrderSummary, name="shopping-cart"),
    path('my-orders/', MyOrders.as_view(), name="my-orders"),
    path('my-orders/<int:order_id>', MyOrderDetail.as_view(), name="my-orders-detail"),

    # PAYMENT AND ETC URLS
    path('webhooks/stripe/', stripe_webhook, name="webhook-stripe"),
    # stripe listen --forward-to http://127.0.0.1:8000/webhooks/stripe/
    path('checkout/', CheckoutPage.as_view(), name="checkout"),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/', SuccessView.as_view(), name='success'),

    # REGISTRATION URLS
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout/', logout_user, name="logout"),

]
