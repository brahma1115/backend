import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.append(os.getcwd())
django.setup()

from api.models import Alert

print("--- FULL ALERT LIST ---")
for alert in Alert.objects.all():
    print(f"ID: {alert.id} | Patient: {alert.patient.full_name} | Type: {alert.alert_type} | Value: {alert.current_value} | Desc: {alert.description}")
print("--- END ---")
