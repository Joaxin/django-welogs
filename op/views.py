from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'op/home.html'


class AboutPageView(TemplateView):
    template_name = 'op/about.html'