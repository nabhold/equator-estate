from django.urls import path, include, re_path
from . views import HomePageView, AboutPageView, ContactPageView


urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('contact/', ContactPageView.as_view(), name='contact'),
    path('', HomePageView.as_view(), name='home'),
]
