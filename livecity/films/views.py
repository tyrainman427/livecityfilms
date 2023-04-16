from django.shortcuts import render
from .forms import ContactForm

# Create your views here.
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

def pricing(request):
    return render(request, 'films/pricing.html')

def services(request):
    return render(request, 'films/services.html')

def now_playing(request):
    return render(request, 'films/now_playing.html')