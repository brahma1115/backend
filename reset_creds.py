import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Profile

def reset_user(username, email, password, role):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.email = email
    user.set_password(password)
    user.save()
    
    profile, p_created = Profile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    
    print(f"User: {username} | Email: {email} | Password: {password} | Role: {role} -> {'CREATED' if created else 'UPDATED'}")

print("Resetting Test Credentials:")
reset_user('doctor1@test.com', 'doctor1@test.com', 'doctor123', 'doctor')
reset_user('doctor2@test.com', 'doctor2@test.com', 'doctor123', 'doctor')
reset_user('admin@test.com', 'admin@test.com', 'admin123', 'adminastrator')
