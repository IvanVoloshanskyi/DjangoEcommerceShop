from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

from backend_ecommerce.models import Item, Review


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-input',
            'placeholder': 'Enter your name here',
            'backgrounnd-image': ''
        }
    ))

    class Meta:
        model = User
        fields = ("username", 'email', "password1", "password1")

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-input'
        self.fields['email'].widget.attrs['class'] = 'form-input'


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password",)

    def __init__(self, *args, **kwargs):
        super(LoginUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['password'].widget.attrs['class'] = 'form-input'


PAYMENT_CHOICES = (('C', 'Cash'),
                   ('B', 'Bank Transfer'),)


class CheckoutForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input',
                                                               }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input',
                                                              }))
    phone_num = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input',
                                                              }))
    country = CountryField(blank_label="Select Country").formfield(
        widget=CountrySelectWidget(attrs={'class': 'checkout-input  country'}))
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    zip = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input', }))


RATING_CHOICES = (
    ('1', ''),
    ('2', ''),
    ('3', ''),
    ('4', ''),
    ('5', ''),
)


class ReviewForm(forms.Form):
    rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': 'rating'}), choices=RATING_CHOICES)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input', 'autocomplete': 'off', }))
    advantages = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input', 'autocomplete': 'off', }))
    disadvantages = forms.CharField(widget=forms.TextInput(attrs={'class': 'checkout-input', 'autocomplete': 'off', }))
