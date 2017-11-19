from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView


class SampleView(TemplateView):
    print('hello')
    template_name = 'classification/index.html'

    def get(self, request, *args, **kwargs):

        ctx = {
            'neko': 'mochi',
            'nuko': 'inu',
        }

        return self.render_to_response(context=ctx)


def func(request):
    return JsonResponse({'hello': 'world'})



