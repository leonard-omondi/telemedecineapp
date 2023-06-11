from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='telemedicine-home'),
    path('about/', views.about, name='telemedicine-about'),
    path('contact/', views.contact, name='telemedicine-contact'),
    path('patientlist/', views.patientlist, name='telemedicine-patientlist'),
    path('appointment_scheduling/', views.appointment_scheduling, name='telemedicine-appointment_scheduling'),
    path('appointment_requested/', views.appointment_requested, name='telemedicine-appointment_requested'),

    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('register/', views.register, name='register'),
    path('patient_registration/', views.patient_register, name='patient-registration'),
    path('doctor_registration/', views.doctor_register, name='doctor-registration'),
    path('employee_registration/', views.employee_register, name='employee_registration'),

]
