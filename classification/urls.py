from django.conf.urls import url

from .views import SampleView, func


urlpatterns = [
    url(r'^$', SampleView.as_view(), name='sample'),
    url(r'^func/', func, name='func'),
]