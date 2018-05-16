from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.templatetags.static import static


def index(request):
    return HttpResponse("Hello, world. You're at the plots index.")

# Create your views here.

# Home page
# Don't have a search function so don't need request and return
class HomeView(generic.base.TemplateView):
    template_name = 'plots/home.html'

# About page
class AboutView(generic.base.TemplateView):
    template_name = 'plots/about.html'

# Contact page
class ContactView(generic.base.TemplateView):
    template_name = 'plots/contact.html'

# Contact page
class Data1View(generic.base.TemplateView):
    template_name = 'plots/data1.html'

# minfo page - interactive

# landscape page - landscapes pre-plotted in JS? And simply displayed?
