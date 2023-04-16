from django.urls import path
from .views import *

app_name = 'films'

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('services/', services, name="services"),
    path('pricing/', Pricing.as_view(), name="pricing"),
    path('contact/', contact, name="contact"),
    path('now_playing/', now_playing, name="now_playing"),
    

    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),

    path('create-checkout-session/<id>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('successful/', Successful.as_view(), name='successful'),
    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),
   
]
