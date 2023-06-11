from django.shortcuts import render
from django.http import HttpResponse
#from .models import Post
from .models import patients

from django.shortcuts import render, redirect
from django.http import HttpResponse
#from .models import Post
from .models import patients, slots, appointments, appointment_date
import datetime
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from .forms import PatientSignUpForm, DoctorSignUpForm, EmployeeSignUpForm, DocumentUploadForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from physicianportal.views import doctorhome

from djangoProjectTelemedicine.decorators import allowed_users
from django.contrib.auth.models import Group

from .models import chartreports
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail


# Handles traffic to our homepage
def home(request):
    if request.method == 'POST':
        ssn = request.POST['ssn']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        middlename = request.POST['middlename']
        dob = request.POST['dob']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']
        address1 = request.POST['address1']
        city = request.POST['city']
        zipcode = request.POST['zipcode']
        state = request.POST['state']
        doctorID = request.POST['doctorID']
        user_id = request.POST['user_id']

        obj = patients()
        obj.ssn = ssn
        obj.lastname = lastname
        obj.firstname = firstname
        obj.middlename = middlename
        obj.dob = dob
        obj.gender = gender
        obj.height = height
        obj.weight = weight
        obj.address1 = address1
        obj.city = city
        obj.zipcode = zipcode
        obj.state = state
        obj.doctorID = doctorID
        obj.user_id = user_id
        obj.save()
    context = {

    }
    return render(request, 'telemedicine/home.html', context)


def about(request):
    return render(request, 'telemedicine/about.html', {'title': 'About'})

@login_required
@allowed_users(allowed_roles=['staff', 'doctor'])
def patientlist(request):
    User = get_user_model()
    current_user = User.objects.get(id=request.user.id)
    if current_user is not None and current_user.is_doctor:
        allpatients = patients.objects.all().filter(doctorID=request.user.id).values('gender', 'user_id__first_name',
                                                                                     'user_id__last_name', 'doctorID','ethnicity', 'weight', 'ssn', 'dob', 'address1','user_id__phone', 'user_id__email')
    elif current_user is not None and current_user.is_staff:
        allpatients = patients.objects.all().values('gender', 'user_id__first_name',
                                                                                     'user_id__last_name', 'doctorID','ethnicity', 'weight', 'ssn', 'dob', 'address1','user_id__phone', 'user_id__email')
    else:
        msg = 'error validating user'
        print(msg)


    context = {
        'patients': allpatients
    }
    return render(request, 'telemedicine/patientlist.html', context)


def contact(request):
    return render(request, 'telemedicine/contact.html')


def patient(request):
    return render(request, 'telemedicine/about.html')


def physician(request):
    return render(request, 'telemedicine/about.html')



@login_required
def appointment_scheduling(request):
    User = get_user_model()
    current_user_id = patients.objects.filter(user_id = request.user.id)[0]
    if request.method == 'POST':
        aptdatetime = request.POST['appointment_date']+" "+request.POST['appointment_slots']
        timeslot=request.POST['appointment_slots']
        print(aptdatetime)
        obj = appointments()
        obj.madeon = datetime.datetime.now()
        obj.aptdatetime = aptdatetime
        obj.patientno=current_user_id
        obj.save()

    context = {
       # 'slots': slots.objects.all().filter(end_time="18:00")
       'slots':slots.objects.all(),
        'current_user_id': current_user_id
    }
    return render(request, 'telemedicine/appointment_scheduling.html', context)


def appointment_requested(request):
    print('Request sent')
    User = get_user_model()
    current_patient_user_id = patients.objects.filter(user_id=request.user.id)[0]
    current_user_id= User.objects.get(id=request.user.id)
    if request.method == 'POST':
        aptdatetime = request.POST['appointment_date'] + " " + request.POST['appointment_slots']
        timeslot = request.POST['appointment_slots']
        print(aptdatetime)
        obj = appointments()
        obj.madeon = datetime.datetime.now()
        obj.aptdatetime = aptdatetime
        obj.patientno = current_patient_user_id
        obj.save()
        firstname = current_user_id.first_name
        lastname=current_user_id.last_name
        email=current_user_id.email

        send_mail(
            'Appointment Request Received',  # subject
            'Your doctor appointment request for '+ aptdatetime +' was received.',  # message
            'ajmosquera2006@gmail.com',  # from email
            [email],  # to email
        )

    context = {
        # 'slots': slots.objects.all().filter(end_time="18:00")
        'slots': slots.objects.all(),
        'current_user_id': current_user_id,
        'aptdatetime': obj.aptdatetime,
        'fname': firstname,
        'lname': lastname,
        'email': email
    }

    return render(request, 'telemedicine/appointment_requested.html', context)


def logout_view(request):
    logout(request)
    return render(request, 'telemedicine//logout.html')


def login_request(request):
    form = AuthenticationForm(data=request.POST or None)
    msg = None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_patient:
            login(request, user)
            return redirect('patienthome')
        elif user is not None and user.is_doctor:
            login(request, user)
            return redirect('doctorhome')
        elif user is not None and user.is_staff:
            login(request, user)
            return redirect('staff-appointmentlist_all')
        else:
            msg = 'error validating form'

    return render(request, 'telemedicine/login.html', {'form': form, 'msg': msg})


def register(request):
    return render(request, 'telemedicine/register.html')

def patient_register(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='patient')
            user.groups.add(group)

            messages.success(request, f'Account created for {username}, you can now log in.')
            return redirect('telemedicine-home')
    else:
        form = PatientSignUpForm()
    return render(request, 'telemedicine/patient_registration.html', {'form': form})


def employee_register(request):
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='staff')
            user.groups.add(group)

            messages.success(request, f'Account created for {username}, you can now log in.')
            return redirect('telemedicine-home')
    else:
        form = EmployeeSignUpForm()
    return render(request, 'telemedicine/employee_registration.html', {'form': form})


def doctor_register(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='doctor')
            print(group)
            user.groups.add(group)

            messages.success(request, f'Account created for {username}, you can now log in.')
            return redirect('telemedicine-home')
    else:
        form = DoctorSignUpForm()
    return render(request, 'telemedicine/doctor_registration.html', {'form': form})








