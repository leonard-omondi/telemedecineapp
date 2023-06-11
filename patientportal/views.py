import os
import time, datetime
import json

import telemedicine
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from telemedicine.models import appointments, patients, doctorstaff, chartreports
from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from pusher import Pusher
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import PatientRegisterForm
from djangoProjectTelemedicine.decorators import allowed_users
from django.contrib.auth.models import Group




def register(request):
    if request.method == 'POST':
        form = PatientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, please log in.')
            return redirect('login')
    else:
        form = PatientRegisterForm()
    return render(request, 'patientportal/register.html', {'form': form})


@login_required
def patienthome(request):
    User = get_user_model()
    User.objects.filter(is_superuser=True).exclude(id=request.user.id).only('id', 'first_name')
    doctorID = get_object_or_404(patients,user_id=request.user.id).doctorID
    current_user_id = patients.objects.filter(user_id = request.user.id)[0]

    context = {
        'allUsers': User.objects.exclude(id=request.user.id).only('id', 'first_name'),
        'next_appointments': appointments.objects.filter(patientno_id=current_user_id).filter(aptdatetime__gte=datetime.datetime.now()).filter(confirmed__isnull=False),
    'past_appointments': appointments.objects.filter(patientno_id=current_user_id).filter(aptdatetime__lte=datetime.datetime.now()),
    'doctorinfo1': doctorstaff.objects.filter(id=doctorID),
    'doctorinfo2': User.objects.filter(id=doctorID).only('last_name'),
    
    }

    return render(request, 'patientportal/patienthome.html', context)



@login_required
def patientprofile(request):
    User = get_user_model()
    #User.objects.filter(is_superuser=True).filter(id=request.user.id),
    current_user_id = patients.objects.filter(user_id = request.user.id)[0]
    doctorID= patients.objects.get(user_id=request.user.id).doctorID
    patientID = patients.objects.get(user_id=request.user.id).id
    context = {
    #'all_users' : User.objects.exclude(id=request.user.id),
    'next_appointments': appointments.objects.filter(patientno_id=current_user_id).filter(aptdatetime__gte=datetime.datetime.now()).filter(confirmed__isnull=False),
    'past_appointments': appointments.objects.filter(patientno_id=current_user_id).filter(aptdatetime__lte=datetime.datetime.now()),
    'doctorinfo1': doctorstaff.objects.filter(id=doctorID),
    'doctorinfo2': User.objects.filter(id=doctorID).only('last_name'),
    'patientinfo': patients.objects.filter(id=patientID).all()
    }
    return render(request, 'patientportal/patientprofile.html', context)
# Instantiate a Pusher Client
pusher_client = Pusher(app_id=os.environ.get('PUSHER_APP_ID'),
                       key=os.environ.get('PUSHER_KEY'),
                       secret=os.environ.get('PUSHER_SECRET'),
                       ssl=True,
                       cluster=os.environ.get('PUSHER_CLUSTER')
                       )



def pusher_auth(request):
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id': request.user.id,
                'name': request.user.username
            }
        })
    return JsonResponse(payload)


def generate_agora_token(request):
    appID = os.environ.get('AGORA_APP_ID')
    appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
    channelName = json.loads(request.body.decode(
        'utf-8'))['channelName']
    userAccount = request.user.username
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)

    return JsonResponse({'token': token, 'appID': appID})


def call_user(request):
    body = json.loads(request.body.decode('utf-8'))

    user_to_call = body['user_to_call']
    channel_name = body['channel_name']
    caller = request.user.id

    pusher_client.trigger(
        'presence-online-channel',
        'make-agora-call',
        {
            'userToCall': user_to_call,
            'channelName': channel_name,
            'from': caller
        }
    )
    return JsonResponse({'message': 'call has been placed'})

@login_required
@allowed_users(allowed_roles=['patient'])
def document_list(request):
    User = get_user_model()
    current_user_id = patients.objects.filter(user_id = request.user.id)[0]
    context = {
        'documents': chartreports.objects.filter(patientno_id=current_user_id)
    }
    return render(request, 'telemedicine/document_list.html', context)