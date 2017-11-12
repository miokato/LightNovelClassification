from django.conf.urls import url

from .views import SampleView


urlpatterns = [
    url(r'^sample/', SampleView.as_view(), name='sample'),
]