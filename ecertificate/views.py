from django.views.generic import TemplateView

#This file is applies the concept of class based views, where each class is linked to a particular template
#basically the template that must be used on the website when the particular class view is called
class HomePage(TemplateView):
    template_name = 'index.html'
    
class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class AboutPage(TemplateView):
    template_name = 'about.html'