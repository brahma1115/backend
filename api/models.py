from django.db import models
from django.contrib.auth.models import User

# Extends standard User model
class Profile(models.Model):
    ROLE_CHOICES = (
        ('adminastrator', 'Administrator'),
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('respiratory_therapist', 'Respiratory Therapist'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)
    hospital = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Patient(models.Model):
    full_name = models.CharField(max_length=200)
    patient_id = models.CharField(max_length=50, unique=True)
    dob = models.CharField(max_length=50) # Use string for easier frontend integration
    gender = models.CharField(max_length=50)
    weight = models.FloatField(null=True, blank=True)
    primary_diagnosis = models.CharField(max_length=255, null=True, blank=True)
    admission_date = models.CharField(max_length=50, null=True, blank=True)
    bed_number = models.CharField(max_length=50, null=True, blank=True)
    attending_physician = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=50, default="Admitted")

    def __str__(self):
        return f"{self.full_name} ({self.patient_id})"

class PatientHistory(models.Model):
    patient = models.ForeignKey(Patient, related_name='history', on_delete=models.CASCADE)
    event_type = models.CharField(max_length=50, default="info") # e.g. alert, treatment, info
    event_title = models.CharField(max_length=255, default="Event")
    event_description = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

class Device(models.Model):
    mac_address = models.CharField(max_length=50, unique=True)
    device_type = models.CharField(max_length=50) # Ventilator, Monitor, etc.
    status = models.CharField(max_length=50, default="Active")
    assigned_patient = models.OneToOneField(Patient, null=True, blank=True, related_name='device', on_delete=models.SET_NULL)
    current_settings = models.JSONField(default=dict, blank=True)

class VitalSign(models.Model):
    patient = models.ForeignKey(Patient, related_name='vitals', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    heart_rate = models.FloatField(null=True, blank=True)
    spo2 = models.FloatField(null=True, blank=True)
    respiratory_rate = models.FloatField(null=True, blank=True)
    blood_pressure_sys = models.FloatField(null=True, blank=True)
    blood_pressure_dia = models.FloatField(null=True, blank=True)
    temperature = models.FloatField(null=True, blank=True)
    
    # Ventilator Specific Readings (activity_monitor_bed.xml)
    ppeak = models.FloatField(null=True, blank=True)
    peep = models.FloatField(null=True, blank=True)
    vte = models.FloatField(null=True, blank=True)
    fio2 = models.FloatField(null=True, blank=True)
    ie_ratio = models.CharField(max_length=20, null=True, blank=True) # e.g., "1:2.0"

class Alert(models.Model):
    patient = models.ForeignKey(Patient, related_name='alerts', on_delete=models.CASCADE)
    device = models.ForeignKey(Device, null=True, blank=True, on_delete=models.SET_NULL)
    alert_type = models.CharField(max_length=50) # Critical, Warning
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Active") # Active, Acknowledged, Resolved
    escalated_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    
    # Alert Details and Parameter Context
    current_value = models.CharField(max_length=50, blank=True, null=True) # e.g. "35 bpm"
    limit_value = models.CharField(max_length=50, blank=True, null=True) # e.g. "30 bpm"
    
    # AI Analysis
    ai_confidence = models.IntegerField(null=True, blank=True) # e.g. 87
    probable_cause = models.TextField(blank=True, null=True)
    suggested_action = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.alert_type} - {self.patient.full_name}"

class AIPredictedEvent(models.Model):
    patient = models.ForeignKey(Patient, related_name='predicted_events', on_delete=models.CASCADE)
    event_name = models.CharField(max_length=200) # e.g. "High Peak Pressure"
    time_to_event = models.CharField(max_length=50) # e.g. "in 2 hours"
    confidence_score = models.IntegerField() # e.g. 87
    recommendation = models.TextField() # e.g. "Check for secretion buildup"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} - {self.patient.full_name}"

class Report(models.Model):
    patient = models.ForeignKey(Patient, related_name='reports', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="Report")
    report_type = models.CharField(max_length=100)
    file_url = models.URLField() # Or FileField
    file_size_bytes = models.IntegerField(default=0) # For displaying e.g. "1.2 MB"
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

class AIChatMessage(models.Model):
    patient = models.ForeignKey(Patient, related_name='chat_messages', on_delete=models.CASCADE, null=True, blank=True)
    sender = models.CharField(max_length=50) # 'user' or 'ai'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Optional structured data for AI responses
    confidence_score = models.IntegerField(null=True, blank=True) # e.g., 92
    likely_causes = models.JSONField(default=list, blank=True) # e.g. [{"cause": "Secretions", "probability": 85}]
    recommended_actions = models.JSONField(default=list, blank=True) # e.g. ["Suction airway", "Verify tube"]

    def __str__(self):
        return f"{self.sender}: {self.message[:20]}"

class PatientRisk(models.Model):
    patient = models.ForeignKey(Patient, related_name='risk_assessments', on_delete=models.CASCADE)
    risk_score = models.IntegerField() # e.g. 87
    risk_factors = models.JSONField(default=list) # e.g. ["High Peak Pressure", "Low Compliance", "Tachypnea"]
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} - Score: {self.risk_score}"

class AlertSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alert_settings')
    
    # Notification Preferences
    push_notifications = models.BooleanField(default=True)
    sound = models.BooleanField(default=True)
    vibration = models.BooleanField(default=True)
    
    # Threshold Defaults
    spo2_low_limit = models.IntegerField(default=90) # percentage
    rr_high_limit = models.IntegerField(default=30) # bpm
    pressure_high_limit = models.IntegerField(default=40) # cmH2O

    def __str__(self):
        return f"Alert Settings for {self.user.username}"

class Anomaly(models.Model):
    patient = models.ForeignKey(Patient, related_name='anomalies', on_delete=models.CASCADE)
    anomaly_type = models.CharField(max_length=100) # e.g., "Waveform Irregularity", "Flow Asynchrony"
    description = models.TextField() # e.g., "Unusual pressure spike detected during expiration phase."
    confidence_score = models.IntegerField() # e.g., 94
    timestamp = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.anomaly_type} - Confidence: {self.confidence_score}%"

class AppearanceSetting(models.Model):
    THEME_CHOICES = (
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
        ('system', 'System Default'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='appearance_settings')
    theme_preference = models.CharField(max_length=20, choices=THEME_CHOICES, default='system')

    def __str__(self):
        return f"Appearance Settings for {self.user.username}"

class FAQ(models.Model):
    selected_topic = models.CharField(max_length=200) # e.g., "How to reset password", "Payment issues"
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.selected_topic

class SupportTicket(models.Model):
    user = models.ForeignKey(User, related_name='support_tickets', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=50, default="Open") # Open, In Progress, Closed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject} ({self.user.username})"

class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    title = models.CharField(max_length=200) # e.g. "Shift Handover", "System Update"
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.user.username}"

class SecuritySetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='security_settings')
    two_factor_auth = models.BooleanField(default=False)
    biometric_login = models.BooleanField(default=False)
    session_timeout_minutes = models.IntegerField(default=15)
    pin_last_changed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Security Settings for {self.user.username}"

class LoginHistory(models.Model):
    user = models.ForeignKey(User, related_name='login_history', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100) # e.g. "iPhone 13", "Web Portal"
    location = models.CharField(max_length=100, blank=True, null=True) # e.g. "New York, USA", "Hospital Wi-Fi"
    login_time = models.DateTimeField(auto_now_add=True)
    is_password_change = models.BooleanField(default=False)

    def __str__(self):
        action = "Password Changed" if self.is_password_change else "Login"
        return f"{action} on {self.device_name} ({self.user.username})"

class OnboardingStep(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_key = models.CharField(max_length=100) # e.g. "img", "img_1", "img_2"
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"Step {self.order}: {self.title}"

class OTP(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.email} - {self.code}"
