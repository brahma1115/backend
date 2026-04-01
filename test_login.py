import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

users = [
    ('doctor1@test.com', 'doctor123'),  # Based on previous common patterns
    ('testuser', 'testpass'),
    ('testuser', '9912249161'), # Use DB password as a guess
]

print("Testing Credentials:")
for username, password in users:
    user = authenticate(username=username, password=password)
    status = "SUCCESS" if user else "FAILED"
    print(f"- User: {username} | Password: {password} | Result: {status}")

# Also check email based login logic
email_to_test = 'doctor1@test.com'
password_to_test = '9912249161' # The MySQL password might be used here too?

try:
    user_obj = User.objects.get(email=email_to_test)
    user = authenticate(username=user_obj.username, password=password_to_test)
    status = "SUCCESS" if user else "FAILED"
    print(f"\nTesting Email Login Logic:")
    print(f"- Email: {email_to_test} | Password: {password_to_test} | Result: {status}")
except User.DoesNotExist:
    print(f"\nUser with email {email_to_test} not found.")
