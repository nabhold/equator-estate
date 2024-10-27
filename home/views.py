from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home/index.html'

class AboutPageView(TemplateView):
    template_name = 'home/about.html'

class ContactPageView(TemplateView):
    template_name = 'home/contact.html'