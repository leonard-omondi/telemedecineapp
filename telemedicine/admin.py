from django.contrib import admin
from .models import patients, user
from .models import immunizations
from .models import medicationsallergies
from .models import prescriptions
from .models import chartreports
from .models import appointments
from .models import visits
from .models import recordings
from .models import slots
from .models import appointment_date
from .models import doctorstaff

admin.site.register(patients)
admin.site.register(immunizations)
admin.site.register(medicationsallergies)
admin.site.register(prescriptions)
admin.site.register(chartreports)
admin.site.register(appointments)
admin.site.register(visits)
admin.site.register(recordings)
admin.site.register(slots)
admin.site.register(appointment_date)
admin.site.register(doctorstaff)
admin.site.register(user)
