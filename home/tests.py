from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from .views import HomePageView, AboutPageView, ContactPageView


# Create your tests here.

class HomePageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('home')
        self.response = self.client.get(url)

    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)


    def test_url_name(self):
        self.assertEqual(self.response.status_code, 200)


    def test_template_name_correct(self):
        self.assertTemplateUsed(self.response, 'home/index.html')
        


class AboutPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('about')
        self.response = self.client.get(url)
    
    
    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)
    
    
    def test_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_correct(self):
        self.assertTemplateUsed(self.response, 'home/about.html')



class ContactPageTests(SimpleTestCase):
    def setUp(self):
        url = reverse('contact')
        self.response = self.client.get(url)
    
    
    def test_url_exists_at_correct_location(self):
        self.assertEqual(self.response.status_code, 200)
    
    
    def test_url_name(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_name_correct(self):
        self.assertTemplateUsed(self.response, 'home/contact.html')
        
        

