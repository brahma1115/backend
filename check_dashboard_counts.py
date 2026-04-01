import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.append(os.getcwd())
django.setup()

from api.models import Patient, Alert, Profile, PatientRisk, AIPredictedEvent

print(f"Total Patients: {Patient.objects.count()}")
print(f"Total Profiles (Staff): {Profile.objects.count()}")
print(f"Active Alerts: {Alert.objects.filter(status='Active').count()}")
print(f"ICU Patients (Active Vents): {Patient.objects.filter(bed_number__icontains='ICU').count()}")
print(f"High Risk Patients (score >= 80): {PatientRisk.objects.filter(risk_score__gte=80).count()}")
print(f"Predictive Events: {AIPredictedEvent.objects.count()}")
