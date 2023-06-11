from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from djangoProjectTelemedicine.decorators import allowed_users
from telemedicine.models import chartreports, appointments, patients, user
from django.core.files.storage import FileSystemStorage
from telemedicine.forms import DocumentUploadForm, UserUpdateForm, PatientUpdateForm, PatientLookupForm
from django.shortcuts import render, redirect
from staff import templates
import datetime
# Create your views here.
from django.contrib import messages

@login_required
@allowed_users(allowed_roles=['staff'])
def document_list(request):
    context = {
        'documents': chartreports.objects.all()
    }
    return render(request, 'staff/document_list_all.html', context)

@login_required
@allowed_users(allowed_roles=['staff'])
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data.values())
            form.save()
            return redirect('staff-documentlist_all')
    else:
        form = DocumentUploadForm
    context = {
        'form': form
    }
    return render(request, 'telemedicine/upload_document.html', context)



@login_required
@allowed_users(allowed_roles=['staff'])
def appointment_list_all(request):
    if request.method == 'POST':
        userinfo = get_user_model()
        record = appointments.objects.get(id=int(request.POST['id']))
        record.checked_on=datetime.datetime.now()
        record.confirmed=request.POST['confirm']
        record.save()
        patientnoid=int(str(record.patientno).split('-')[0])
        email=userinfo.objects.all().filter(id=patientnoid).values('email').all()[0]['email']
        print(record.confirmed)
        aptdatetime= str(record.aptdatetime)

        if record.confirmed=='True':
            send_mail(
                'Appointment Request',  # subject
                'Your doctor appointment request for '+ aptdatetime +' was accepted.',  # message
                'ajmosquera2006@gmail.com',  # from email
                [email],  # to email

            )
        elif record.confirmed=='False':
            send_mail(
                'Appointment Request',  # subject
                'Your doctor appointment request for ' + aptdatetime + ' was denied.',  # message
                'ajmosquera2006@gmail.com',  # from email
                [email],  # to email

            )

    context = {
        'appointments': appointments.objects.all().filter(confirmed__isnull=True).values('id','madeon','aptdatetime','patientno_id', 'patientno__doctorID', 'patientno__user_id__last_name', 'patientno__user_id__first_name'),
    }
    return render(request, 'staff/appointments_list_all.html', context)

@login_required
@allowed_users(allowed_roles=['staff','patient', 'doctor'])
def edit_user_info(request):
    User = get_user_model()
    instanceuser=User.objects.get(id=request.user.id)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=instanceuser)
        if u_form.is_valid() :
            u_form.save()
            messages.success(request, f'The account has been updated')
            return redirect('telemedicine-home')

    else:
        u_form = UserUpdateForm(instance=instanceuser)


    context = {
        'u_form': u_form,
    }
    return render(request, 'staff/edit_user_info.html', context)

@allowed_users(allowed_roles=['staff'])
def edit_patient_info(request):
    User=get_user_model()
    uid= int(request.POST['user_id'])
    print(uid)
    #uid = 7

    patientID=patients.objects.get(user_id=uid)
    userID= User.objects.get(id=uid)
    ssn=patientID.ssn
    dob=patientID.dob
    height=patientID.height
    weight=patientID.weight
    ethnicity=patientID.ethnicity
    doctorID=patientID.doctorID
    address1=patientID.address1
    city=patientID.city
    zipcode=patientID.zipcode
    state=patientID.state
    gender=patientID.gender
    user_str=userID


    if request.method == 'POST':
        p_form = PatientUpdateForm(request.POST, instance=patientID)
        if p_form.is_valid() :

            messages.success(request, f'The account has been updated')
            return redirect('telemedicine-patientlist')


    context = {
    'uid':uid,
    'ssn':ssn,
    'user_str':user_str,
    'dob' :dob,
    'height': height,
    'weight':weight,
    'ethnicity':ethnicity,
    'doctorID':doctorID,
    'address1':address1,
    'city':city,
    'zipcode':zipcode,
    'state':state,
    'gender':gender

    }
    return render(request, 'staff/edit_patient_info.html', context)

@login_required
@allowed_users(allowed_roles=['staff'])
def patient_lookup(request):
    if request.method == 'POST':
        form = PatientLookupForm(request.POST)

        if form.is_valid():
            uid= int(str(form.cleaned_data.values()).split('-')[0].split(':')[1])
            return redirect('staff-edit_patient_info')
    else:
        form = PatientLookupForm

    context = {
        'form': form,

    }
    return render(request, 'staff/patient_lookup.html', context)

