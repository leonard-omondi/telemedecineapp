from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from django.http import request

from .models import chartreports, user
from phone_field import PhoneField
import datetime

from django.contrib.auth.forms import UserCreationForm
from .models import patients, doctorstaff


class PatientSignUpForm(UserCreationForm):  # Username, password1, password2 provided by default
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = PhoneField(blank=True)
    email = forms.EmailField(max_length=254)
    ssn = forms.IntegerField(max_value=999999999, required=True)
    dob = forms.DateField(required=True)
    gender_choices = [('f', 'Female'),('m', 'Male'),('NA', 'NA')]
    gender=forms.CharField(widget=forms.Select(choices=gender_choices))
    address = forms.CharField()
    city=forms.CharField()
    state=forms.CharField(required=True)
    zipcode=forms.IntegerField(max_value=99999, required=True)

    class Meta(UserCreationForm.Meta):
        model = user
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'ssn', 'dob', 'gender', 'address', 'city', 'zipcode', 'state']

    @transaction.atomic  # Saves an instance of our form
    def save(self):
        newuser = super().save(commit=False)
        newuser.is_patient = True
        newuser.is_staff = False
        newuser.is_doctor = False
        newuser.first_name = self.cleaned_data.get('first_name')
        newuser.last_name = self.cleaned_data.get('last_name')
        newuser.phone = self.cleaned_data.get('phone')
        newuser.email = self.cleaned_data.get('email')
        newuser.save()
        #newuser_userid= newuser.objects.get(id)
        #print(newuser_userid)
        patient = patients.objects.create(user_id=newuser, ssn = self.cleaned_data.get('ssn'),dob = self.cleaned_data.get('dob'), address1= self.cleaned_data.get('address'), city=self.cleaned_data.get('city'), zipcode=self.cleaned_data.get('zipcode'), state=self.cleaned_data.get('state'),gender= self.cleaned_data.get('gender'))
        #patient.save()
        return newuser

class DoctorSignUpForm(UserCreationForm):  # Username, password1, password2 provided by default
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = forms.EmailField(max_length=254)
    discipline = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = user
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'discipline']

    @transaction.atomic
    def save(self):
        newuser = super().save(commit=False)
        newuser.is_patient = False
        newuser.is_staff = False
        newuser.is_doctor = True
        newuser.first_name = self.cleaned_data.get('first_name')
        newuser.last_name = self.cleaned_data.get('last_name')
        newuser.phone = self.cleaned_data.get('phone')
        newuser.email = self.cleaned_data.get('email')
        newuser.save()
        doctor = doctorstaff.objects.create(id=newuser, discipline = self.cleaned_data.get('discipline'))

        # doctor.employee_id = self.cleaned_data.get('user_id')
        #doctor.save()
        return newuser


class EmployeeSignUpForm(UserCreationForm):  # Username, password1, password2 provided by default
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = forms.EmailField(max_length=254)
    discipline = forms.CharField(required=True)

    class Meta(UserCreationForm.Meta):
        model = user
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone', 'discipline']

    @transaction.atomic
    def save(self):
        newuser = super().save(commit=False)
        newuser.is_patient = False
        newuser.is_staff = True
        newuser.is_doctor = False
        newuser.first_name = self.cleaned_data.get('first_name')
        newuser.last_name = self.cleaned_data.get('last_name')
        newuser.phone = self.cleaned_data.get('phone')
        newuser.email = self.cleaned_data.get('email')
        newuser.save()
        staff = doctorstaff.objects.create(id=newuser, discipline = self.cleaned_data.get('discipline'))
        # employee.employee_id = self.cleaned_data.get('user_id')
        staff.save()
        return newuser



class UserUpdateForm(forms.ModelForm):
    id=forms.HiddenInput
    #uid=id
    username = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    middle_name = forms.CharField(required=False)
    last_name = forms.CharField(required=True)
    phone = PhoneField(blank=True)
    email = forms.EmailField(max_length=254)
    #discipline = forms.CharField(required=True)



    class Meta:
        model = user
        fields = ['id','first_name', 'middle_name', 'last_name', 'phone', 'username', 'email']

       # def update(self):
        #    discipline = doctorstaff.objects.update(id=uid, discipline=self.cleaned_data.get('discipline'))


class PatientUpdateForm(forms.ModelForm):
    id = forms.IntegerField()
    ssn = forms.IntegerField(max_value=999999999, required=True)
    dob = forms.DateField(required=True)
    gender_choices = [('f', 'Female'),('m', 'Male'),('NA', 'NA')]
    gender=forms.CharField(widget=forms.Select(choices=gender_choices))
    address1 = forms.CharField()
    city=forms.CharField()
    state=forms.CharField(required=True)
    zipcode=forms.IntegerField(max_value=99999, required=True)

    class Meta:
        model = patients
        fields = ['id', 'ssn','dob','gender','address1','city','state','zipcode']
        #staff = doctorstaff.objects.update()

class PatientLookupForm(forms.ModelForm):

    class Meta:
        model = patients
        fields = ['user_id']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = chartreports
        fields = ('patientno', 'filename', 'fileurl', 'notes')



