from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView

from classification.tools.parser import MessageManager, CabochaParser
from classification.tools.predict import Predictor


class SampleView(TemplateView):
    template_name = 'classification/index.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, 'classification/index.html', context=self.context)

    def post(self, request):
        manager = MessageManager(CabochaParser())
        predictor = Predictor()

        text = request.POST.get('message')
        mes = manager.extract_message(text)
        words = mes.bags
        prediction = predictor.predict(words)
        print(prediction)
        self.context['answer'] = prediction
        self.context['text'] = text
        return self.render_to_response(context=self.context)


def func(request):
    return JsonResponse({'hello': 'world'})



