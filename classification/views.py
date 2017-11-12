from django.shortcuts import render
from django.views.generic import TemplateView


class SampleView(TemplateView):
    print('hello')
    template_name = 'classification/index.html'


