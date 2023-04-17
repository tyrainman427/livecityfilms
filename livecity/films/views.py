from django.http.response import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from .models import *
from django.views.generic import ListView, CreateView, DetailView, TemplateView
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import ContactForm

from django.http import JsonResponse
from django.views import View


stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, 'films/index.html')

def about(request):
    return render(request, 'films/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'films/success.html')
    form = ContactForm()
    context = {'form': form}

    return render(request, 'films/contact.html', context)

# def pricing(request):
#     return render(request, 'films/pricing.html')

class Pricing(TemplateView):
    model = Product
    template_name = "films/pricing.html"
    pk_url_kwarg = 'id'

    # def get_context_data(self, **kwargs):
    #     context = super(Pricing, self).get_context_data(**kwargs)
    #     context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
    #     return context  
    def get_context_data(self, **kwargs):
        products = Product.objects.all()
     
        context = super(Pricing,
                        self).get_context_data(**kwargs)
        context.update({
            "products": products,
        
        })
        return context

def services(request):
    return render(request, 'films/services.html')

def now_playing(request):
    return render(request, 'films/now_playing.html')

# @csrf_exempt
# def create_checkout_session(request, id):

#     request_data = json.loads(request.body)
#     product = get_object_or_404(Product, pk=id)

#     stripe.api_key = settings.STRIPE_SECRET_KEY
class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs["id"])
        domain = "https://yourdomain.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
        # Customer Email is optional,
        # It is not safe to accept email directly from the client side
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': product.name,
                     'description': product.description,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=domain + '/success/',
        cancel_url=domain + '/cancel/',
    )

    # OrderDetail.objects.create(
    #     customer_email=email,
    #     product=product, ......
    # )

        order = OrderDetail()
        order.product = product
        order.stripe_payment_intent = checkout_session['payment_intent']
        order.amount = int(product.price * 100)
        order.save()

        # return JsonResponse({'data': checkout_session})
        # return JsonResponse({'sessionId': checkout_session.id})
        return redirect(checkout_session.url)


class PaymentSuccessView(TemplateView):
    template_name = "films/payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "films/payment_failed.html"

class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "films/order_history.html"
    

class CancelView(TemplateView):
    template_name = "films/cancel.html"
    
class Successful(TemplateView):
    template_name = "films/successful.html"
    
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get('session_id')
        if session_id is None:
            return HttpResponseNotFound()
        
        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.payment_intent)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)
    
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]

        # TODO - send an email to the customer

    return HttpResponse(status=200)