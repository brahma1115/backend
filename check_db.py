import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Profile, Patient, Device, VitalSign, Alert

print("Users and Profiles:")
for user in User.objects.all():
    profile = Profile.objects.filter(user=user).first()
    role = profile.role if profile else "No Profile"
    print(f"- {user.username} | Email: {user.email} | Role: {role}")

print("\n--- Data Counts ---")
print(f"Patients: {Patient.objects.count()}")
print(f"Vital Signs: {VitalSign.objects.count()}")
print(f"Alerts: {Alert.objects.count()}")
