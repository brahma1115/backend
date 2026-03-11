from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Patient, PatientHistory, Device, VitalSign, Alert, AIPredictedEvent, Report, AIChatMessage, PatientRisk, AlertSetting, Anomaly, AppearanceSetting, FAQ, SupportTicket

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

class PatientSerializer(serializers.ModelSerializer):
    formatted_details = serializers.SerializerMethodField()
    formatted_bed = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = '__all__'

    def get_formatted_details(self, obj):
        # "ID: P001 • 65y"
        # Mocking or calculating age if dob exists
        age = "65y"
        if obj.dob:
            try:
                from dateutil.parser import parse
                from django.utils import timezone
                dob_dt = parse(obj.dob)
                age = f"{timezone.now().year - dob_dt.year}y"
            except:
                pass
        return f"ID: {obj.patient_id} • {age}"

    def get_formatted_bed(self, obj):
        return f"Bed: {obj.bed_number}"

class PatientHistorySerializer(serializers.ModelSerializer):
    timestamp_display = serializers.SerializerMethodField()

    class Meta:
        model = PatientHistory
        fields = '__all__'

    def get_timestamp_display(self, obj):
        from django.utils import timezone
        import datetime
        
        now = timezone.now()
        if obj.timestamp.date() == now.date():
            return obj.timestamp.strftime("%H:%M Today")
        elif obj.timestamp.date() == (now - datetime.timedelta(days=1)).date():
            return obj.timestamp.strftime("%H:%M Yesterday")
        return obj.timestamp.strftime("%H:%M %b %d")

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class VitalSignSerializer(serializers.ModelSerializer):
    mean_arterial_pressure = serializers.SerializerMethodField()

    class Meta:
        model = VitalSign
        fields = '__all__'

    def get_mean_arterial_pressure(self, obj):
        if obj.blood_pressure_sys and obj.blood_pressure_dia:
            return round((obj.blood_pressure_sys + 2 * obj.blood_pressure_dia) / 3, 1)
        return None

class AlertSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    bed_number = serializers.CharField(source='patient.bed_number', read_only=True)
    
    class Meta:
        model = Alert
        fields = '__all__'

class AIPredictedEventSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    bed_number = serializers.CharField(source='patient.bed_number', read_only=True)
    
    class Meta:
        model = AIPredictedEvent
        fields = '__all__'

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class AIChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIChatMessage
        fields = '__all__'

class PatientRiskSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    bed_number = serializers.CharField(source='patient.bed_number', read_only=True)

    class Meta:
        model = PatientRisk
        fields = '__all__'

class AlertSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertSetting
        fields = '__all__'

class AnomalySerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    bed_number = serializers.CharField(source='patient.bed_number', read_only=True)

    class Meta:
        model = Anomaly
        fields = '__all__'

class AppearanceSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppearanceSetting
        fields = '__all__'

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'

from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

from .models import SecuritySetting, LoginHistory

class SecuritySettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySetting
        fields = '__all__'

class LoginHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginHistory
        fields = '__all__'

from .models import OnboardingStep

class OnboardingStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingStep
        fields = '__all__'

from .models import OTP

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'
