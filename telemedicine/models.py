from django.db import models
from django.utils import timezone
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import datetime

class user(AbstractUser):  # Extends the default model with the help of AbstractUser
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=254)
    phone = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{} - {}- {}".format(self.id, self.last_name, self.first_name)
    class Meta:
        managed = True
        db_table = 'telemedicine_user'


class patients(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    ssn = models.PositiveIntegerField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    height = models.FloatField( blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    ethnicity = models.CharField(max_length=20, blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True)
    smoking = models.BooleanField(blank=True, null=True)
    familyhistory = models.TextField(blank=True, null=True)
    address1 = models.CharField(max_length=50, blank=True, null=True)
    address2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    weight = models.FloatField( blank=True, null=True)
    doctorID=models.IntegerField(null=True)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    def __str__(self):
        return "{} - {}- {}".format(self.user_id.id, self.user_id.last_name,self.user_id.first_name)


class immunizations(models.Model):
    patientno=models.ForeignKey(patients, on_delete=models.CASCADE)
    immunizations=models.TextField(max_length=200)
    dateimmunization=models.DateField()


class medicationsallergies(models.Model):
    patientno=models.ForeignKey(patients, on_delete=models.CASCADE)
    medications=models.TextField(max_length=200)
    enddatemedications=models.DateField()
    allergies=models.TextField(max_length=200)

class prescriptions(models.Model):
    patientno=models.ForeignKey(patients, on_delete=models.CASCADE)
    medicinename=models.TextField(max_length=200)
    dosage=models.CharField(max_length=200)
    startdate = models.DateField()
    enddate=models.DateField()

class chartreports(models.Model):
    patientno=models.ForeignKey(patients, on_delete=models.CASCADE, default=2)
    filename=models.CharField(max_length=50)
    notes=models.TextField(max_length=250, blank=True)
    fileurl=models.FileField(upload_to='documents/patientreports')
    date=models.DateTimeField(default=datetime.datetime.now(), blank=True)

class appointments(models.Model):
    patientno=models.ForeignKey(patients, on_delete=models.CASCADE)
    madeon=models.DateField()
    aptdatetime=models.DateTimeField()
    #checked_by_staff_on=models.DateField(default=blank=True)
    confirmed=models.BooleanField(blank=True, null=True)

class visits(models.Model):
    appointmentno=models.ForeignKey(appointments, on_delete=models.CASCADE)
    date=models.DateField()
    time=models.TimeField(default=00)
    symptom=models.TextField(max_length=200)
    condition=models.TextField(max_length=200)
    notes=models.TextField(max_length=500)
    followupbool=models.BooleanField(default=False)

class recordings(models.Model):
    visitno=models.ForeignKey(visits, on_delete=models.CASCADE)
    videoURL=models.URLField()
    messageURL=models.URLField()

class slots(models.Model):
    id = models.PositiveIntegerField(null=False, primary_key=True)
    start_time = models.TextField()
    end_time = models.TextField()

class appointment_date(models.Model):
    id = models.PositiveIntegerField(null=False, primary_key=True)
    date = models.DateField(blank=True, null=True)
    timeslot_id = models.IntegerField(blank=True, null=True)
    taken = models.BooleanField(blank=True, null=True)


class doctorstaff(models.Model):
    #models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    id = models.ForeignKey(user, on_delete=models.CASCADE, null=False, primary_key=True, db_column='id')
    discipline = models.CharField(max_length=150, blank=True, null=True)









