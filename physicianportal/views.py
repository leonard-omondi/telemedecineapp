import json
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

from pusher import Pusher

from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from djangoProjectTelemedicine.decorators import allowed_users
import time
from telemedicine.models import appointments, patients, doctorstaff, chartreports, user


@login_required
@allowed_users(allowed_roles=['doctor'])
def doctorhome(request):
    User = get_user_model() 
    patientlist = []

    docs_patients = patients.objects.filter(doctorID = request.user.id).values('user_id')
    for patient in docs_patients:
        patientlist.append((int) (patient['user_id']))
    print('patientlist',patientlist)
    doctor_patients = User.objects.filter(id__in=patientlist)
    return render(request, 'physicianportal/doctorhome.html',{'docs_users':doctor_patients})


@login_required
@allowed_users(allowed_roles=['doctor'])
def doctorprofile(request):
    User = get_user_model()
    
    return render(request, 'physicianportal/doctorprofile.html')

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

