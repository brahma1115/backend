import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

email = 'bhargav2001@gmail.com'
try:
    user = User.objects.get(email=email)
    print(f"User found: {user.username} (Email: {user.email})")
except User.DoesNotExist:
    print(f"User NOT found for email: {email}")
