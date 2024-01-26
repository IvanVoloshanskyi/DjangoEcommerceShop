import json
import stripe
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, resolve, reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from core import settings
from .forms import RegisterUserForm, LoginUserForm, CheckoutForm, ReviewForm
from .models import Item, OrderItem, Order, CheckoutDetails, Review, Payment

stripeToken = stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'


class HomePage(View):
    def get(self, *args, **kwargs):
        if 'search' in self.request.GET:
            search = self.request.GET.get('search')
            q = Item.objects.filter(title__icontains=search, is_published=True)
        else:
            q = Item.objects.filter(is_published=True)
        context = {'object_list': q,
                   }
        return render(self.request, 'index.html', context)


class ItemPage(DetailView):
    model = Item
    template_name = 'item.html'
    pk_url_kwarg = 'item_id'

    def tabs(self, item_id, *args, **kwargs):
        item = get_object_or_404(Item, pk=item_id)
        context = {'object': item,
                   'current_urlname': resolve(self.request.path).url_name
                   }
        return render(self.request, 'inc/_tabs.html', context)


class MyOrders(LoginRequiredMixin, ListView):
    login_url = '/login/'
    paginate_by = 8
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, ordered=True).prefetch_related(
            "items__item").select_related("user").order_by("-id")


class MyOrderDetail(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    template_name = "my_orders/my_order_detail.html"
    model = Order
    pk_url_kwarg = "order_id"
    context_object_name = "element"

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset.prefetch_related("items__item")


class ItemDescription(DetailView):
    model = Item
    template_name = 'item_description.html'
    pk_url_kwarg = 'item_id'


def ItemReview(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    review = Review.objects.filter(item_id=item_id).select_related('user')

    form = ReviewForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.cleaned_data.get('comment')
            advantages = form.cleaned_data.get('advantages')
            disadvantages = form.cleaned_data.get('disadvantages')
            rating = form.cleaned_data.get('rating')
            data = Review(user=request.user, item=item, comment=comment, advantages=advantages,
                          disadvantages=disadvantages, stars=rating)
            data.save()
            return redirect('item-review', item_id=item.id)
        else:
            form = ReviewForm()

    context = {'object': item,
               'review': review,
               'form': form,
               }
    return render(request, 'item_review.html', context)


@login_required(login_url=reverse_lazy("login"))
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item.quantity += 1
            order_item.save()
            return redirect("shopping-cart")
        else:
            order.items.add(order_item)
            return redirect("shopping-cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect("shopping-cart")


@login_required(login_url=reverse_lazy("login"))
def remove_single_item_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
                order_item.delete()
            return redirect("shopping-cart")
        else:
            return redirect("shopping-cart")
    else:
        return redirect("shopping-cart")


@login_required(login_url=reverse_lazy("login"))
def remove_from_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__id=item.id).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # remove the order item from the order
            order.items.remove(order_item)
            order_item.delete()
            return redirect("shopping-cart")
        else:
            return redirect("shopping-cart")
    else:
        return redirect("shopping-cart")


class ItemCategory(ListView):
    model = Item
    template_name = 'category_page.html'
    pk_url_kwarg = 'category_id'
    context_object_name = 'categories'

    def get_queryset(self):
        return Item.objects.filter(category__id=self.kwargs['category_id'], is_published=True)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "registration/login.html"

    def get_success_url(self):
        return reverse_lazy("homepage")


def logout_user(request):
    logout(request)
    return redirect("/")


@login_required(login_url='login')
def OrderSummary(request):
    order = Order.objects.filter(user=request.user, ordered=False).prefetch_related('items__item').first()
    if order:
        return render(request, 'shopping_cart.html', {'object': order})
    else:
        return render(request, 'shopping_cart.html')


@csrf_exempt
def create_checkout_session(request):
    cart = Order.objects.filter(user=request.user, ordered=False).first()

    if cart is None or cart.items.count() == 0:
        return redirect('shopping-cart')

    line_items = []
    for item in cart.items.all():
        line_items.append(
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.item.title,
                        'description': item.item.description,
                        'images': [request.build_absolute_uri(item.item.photo.url)],
                        # localhost photos are not supported
                    },
                    'unit_amount': int(item.item.price * 100),
                },
                'quantity': item.quantity
            }
        )

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
        metadata={
            'user_id': request.user.id,
            'order_id': cart.id
        }
    )

    # Return the session ID as a JSON response
    return JsonResponse({'sessionId': session.id})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), settings.STRIPE_WEBHOOK_KEY
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    if event.type == 'checkout.session.completed':
        session = event.data.object
        metadata = session.metadata
        user_id = metadata.get("user_id")
        try:
            order_items = OrderItem.objects.filter(user_id=user_id)
            orders = Order.objects.filter(user_id=user_id)

        except Order.DoesNotExist:
            return HttpResponse(status=404)
        for order in orders:
            payment = Payment.objects.create(order=order, stripe_id=session.payment_intent)
            order.ordered = True
            order.ordered_date = timezone.now()
            order.save()
            payment.save()
        for order_item in order_items:
            order_item.ordered = True
            order_item.save()
    return HttpResponse(status=200)


class CheckoutPage(View):
    def get(self, *args, **kwargs):
        ordered_items = Order.objects.filter(user=self.request.user, ordered=False).prefetch_related('items').first()
        if ordered_items is None:
            return redirect('shopping-cart')
        form = CheckoutForm()
        context = {
            'form': form,
            'ordered_items': ordered_items,
        }
        return render(self.request, "payment/checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            orders = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                phone_num = form.cleaned_data.get('phone_num')
                country = form.cleaned_data.get('country')
                payment_option = form.cleaned_data.get('payment_option')
                zip = form.cleaned_data.get('zip')
                checkout_details = CheckoutDetails(user=self.request.user,
                                                   first_name=first_name,
                                                   last_name=last_name,
                                                   phone_num=phone_num,
                                                   country=country,
                                                   payment_option=payment_option,
                                                   zip=zip,
                                                   )
                checkout_details.save()
                orders.checkout_details = checkout_details
                orders.save()
                if payment_option == 'B':
                    return redirect('create-checkout-session')
                elif payment_option == 'C':
                    orders.ordered = True
                    orders.save()
                    for item in orders.items.all():
                        item.ordered = True
                        item.save()
                    return redirect('success')
                else:
                    return redirect('shopping-cart')

            return render(self.request, "shopping_cart.html")
        except ObjectDoesNotExist:
            return redirect('homepage')


class SuccessView(TemplateView):
    template_name = "payment/success.html"


class CancelView(TemplateView):
    template_name = "payment/cancel.html"
