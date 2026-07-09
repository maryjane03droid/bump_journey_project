from django.contrib import admin
from .models import Appointment, StaffNote, AuditTrail

admin.site.register(Appointment)
admin.site.register(StaffNote)
admin.site.register(AuditTrail)
