import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
sys.path.append(os.getcwd())
django.setup()

from api.models import Alert

print("Recent Alerts in Database:")
for alert in Alert.objects.all().order_by('-timestamp')[:10]:
    print(f"ID: {alert.id} | Patient: {alert.patient.full_name} | Type: {alert.alert_type} | Value: {alert.current_value} | Desc: {alert.description}")
