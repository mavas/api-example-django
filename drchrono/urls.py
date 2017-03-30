from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf import settings

from drchrono import views


urlpatterns = [
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^$', views.home, name='home'),
    #url(r'^oauth2callback$', views.auth_return),
    url(r'^oauth2callback2/$', views.oauth2callback),
    url(r'^patient_checkin/$', views.patient_checkin, name='patient_checkin'),
    url(r'^doctor/$', views.doctor, name='doctor_page'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
