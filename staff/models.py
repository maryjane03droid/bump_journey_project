from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('SCHEDULED', 'Scheduled'),
        ('REFERRED', 'Referred'),
        ('LOCKED', 'Locked'),
        ('NEEDS_DOCTOR_ATTENTION', 'Needs Doctor Attention'),
        ('NEEDS_MIDWIFE_ATTENTION', 'Needs Midwife Attention'),
        ('NEEDS_NUTRITIONIST_ATTENTION', 'Needs Nutritionist Attention'),
        ('NEEDS_LAB_ATTENTION', 'Needs Lab Attention'),
        ('NEEDS_THERAPIST_ATTENTION', 'Needs Therapist Attention'),
        ('COMPLETED', 'Completed'),
        ('REVIEWED', 'Reviewed'),
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')

    doctor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='scheduled_appointments',
        null=True,
        blank=True
    )

    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=35, choices=STATUS_CHOICES, default='REQUESTED')

    # Case locking
    is_locked = models.BooleanField(default=False)
    locked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='locked_appointments'
    )

    # Referral fields
    referred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals_sent'
    )
    referred_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referrals_received'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        doctor_name = self.doctor.username if self.doctor else "Unassigned"
        return f"{self.patient.username} - {self.status} ({doctor_name})"


class StaffNote(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='staff_notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_notes', null=True)
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notes'
    )
    notes = models.TextField()
    prescriptions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        author_name = self.author.username if self.author else "Unknown"
        return f"Note for {self.patient.username} by {author_name}"


class AuditTrail(models.Model):
    ACTION_CHOICES = [
        ('PROFILE_CREATED', 'Profile Created'),
        ('VITALS_ADDED', 'Vitals Added'),
        ('VITALS_UPDATED', 'Vitals Updated'),
        ('VITALS_DELETED', 'Vitals Deleted'),
        ('APPOINTMENT_REQUESTED', 'Appointment Requested'),
        ('APPOINTMENT_SCHEDULED', 'Appointment Scheduled'),
        ('APPOINTMENT_COMPLETED', 'Appointment Completed'),
        ('CASE_LOCKED', 'Case Locked'),
        ('CASE_REFERRED', 'Case Referred'),
        ('STAFF_REGISTERED', 'Staff Registered'),
        ('STAFF_APPROVED', 'Staff Approved'),
        ('NOTE_ADDED', 'Note Added'),
        ('CONTACT_MESSAGE_SENT', 'Contact Message Sent'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_actions')
    user_role = models.CharField(max_length=20)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    patient = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_records'
    )
    description = models.TextField(blank=True, null=True)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"