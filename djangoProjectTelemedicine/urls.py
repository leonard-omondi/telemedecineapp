"""djangoProjectTelemedicine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('telemedicine/', include('telemedicine.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
import agora
from patientportal import views as patientportal_views
from physicianportal import views as physicianportal_views
from staff import views as staff_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('patienthome/', patientportal_views.patienthome, name='patienthome'),
    path('patientprofile/', patientportal_views.patientprofile, name='patientprofile'),
    path('doctorhome/',physicianportal_views.doctorhome,name='doctorhome'),
    path('doctorprofile/',physicianportal_views.doctorprofile,name='doctorprofile'),
    path('', include('telemedicine.urls')),  # Empty path makes this our homepage
    # Agora Routes
    path('', include('agora.urls')),
    path('upload/', staff_views.upload_document, name='telemedicine-upload_document'),
    path('documentlist/', patientportal_views.document_list, name='telemedicine-documentlist'),
    path('documentlist_all/', staff_views.document_list, name='staff-documentlist_all'),
    path('appointmentlist_all/', staff_views.appointment_list_all, name='staff-appointmentlist_all'),
    path('edituserinfo/', staff_views.edit_user_info, name='staff-edit_user_info'),
    path('editpatientinfo/', staff_views.edit_patient_info, name='staff-edit_patient_info'),
    path('patientlookupedit/', staff_views.patient_lookup, name='staff-patient_lookup'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)