from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf import settings

from drchrono import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^patient_home/$', views.patient_home, name='patient_home'),
    url(r'^patient_checkin/(?P<appointment_id>.+)$', views.patient_checkin, name='patient_checkin'),
    url(r'^select_appointment/(?P<patient_id>.+)$', views.select_appointment, name='select_appointment'),
    url(r'^doctor/$', views.doctor, name='doctor_page'),
    url(r'^clear_session/$', views.clear_session, name='clear_session'),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
