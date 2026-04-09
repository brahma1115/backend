import random
import datetime
from django.utils import timezone
from django.db.models import Q
from dateutil.parser import parse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token 
from .models import (Profile, Patient, PatientHistory, Device, VitalSign, Alert, 
                     AIPredictedEvent, Report, SecuritySetting, LoginHistory, OnboardingStep, OTP, Notification, AuditLog) 
from .serializers import (UserSerializer, PatientSerializer, PatientHistorySerializer, 
                          DeviceSerializer, VitalSignSerializer, AlertSerializer, 
                          AIPredictedEventSerializer, ReportSerializer, 
                          SecuritySettingSerializer, LoginHistorySerializer, OnboardingStepSerializer, OTPSerializer, AuditLogSerializer)

from rest_framework_simplejwt.tokens import RefreshToken

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        identifier = request.data.get("email") or request.data.get("username")
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"error": "Email/Username and password are required"}, status=400)

        # Single-pass optimized lookup for Email, Username, or Phone
        user_obj = User.objects.filter(
            Q(email=identifier) | 
            Q(username=identifier) | 
            Q(profile__phone_number=identifier)
        ).select_related('profile').first()
        
        if not user_obj:
            return Response({"error": "Invalid credentials"}, status=401)

        user = authenticate(username=user_obj.username, password=password)

        if user:
            # Check if user is approved by Admin
            profile = getattr(user, 'profile', None)
            if profile and not profile.is_approved and profile.role != 'adminastrator':
                return Response({"error": "Your account is pending administrator approval."}, status=status.HTTP_403_FORBIDDEN)

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        # Handle logout by deleting individual token if needed (though JWT is stateless)
        # Using SimpleJWT, we don't necessarily delete tokens on server, 
        # but for this prototype we'll just return success.
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['DELETE'], permission_classes=[IsAuthenticated])
    def delete_account(self, request):
        user = request.user
        user.delete() # Cascades to profile and other related data
        return Response({"message": "Account deleted successfully"}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'])
    def register(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password")
        full_name = request.data.get("full_name", "")
        phone = request.data.get("phone", "")
        role = request.data.get("role", "nurse") # default to nurse if not provided
        
        # In a real app we'd validate the confirm_password here too if sent from UI
        # We use email as the username for simplicity of login
        username = email 
        
        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        confirm_password = request.data.get("confirm_password")
        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({"error": "An account with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Split full name
        name_parts = full_name.split(" ", 1)
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Map Android UI Role string to backend role code
        role_map = {
            "Doctor": "doctor",
            "Doctor / Physician": "doctor",
            "Nurse": "nurse",
            "Respiratory Therapist": "respiratory_therapist",
            "Administrator": "adminastrator" 
        }
        
        backend_role = role_map.get(role, role.lower().replace(" ", "_"))

        Profile.objects.create(user=user, role=backend_role, phone_number=phone, is_approved=False)
        
        # Notify Admin about new signup
        admin = User.objects.filter(profile__role='adminastrator').first()
        if admin:
            Notification.objects.create(
                user=admin,   
                title="New User Signup",
                message=f"{full_name} has requested access as a {role}.",
                target_user_id=user.id
            )

        return Response({
            "message": "Registration successful. Please wait for administrator approval.",
            "is_pending": True
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        if not User.objects.filter(email=email).exists():
            return Response({"error": "No account found with this email"}, status=status.HTTP_404_NOT_FOUND)
        
        # Prototype: generate a random 6-digit code
        code = str(random.randint(100000, 999999))
        
        OTP.objects.create(email=email, code=code)
        
        # --- IMPORTANT FOR TESTING ---
        # Print clearly to the Django terminal so the user can easily find it
        setup_warning = ""
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            # Check if user has updated the placeholder password
            if getattr(settings, 'EMAIL_HOST_PASSWORD', '') == 'your_app_password':
                setup_warning = " (NOTE: Email not sent. You must update EMAIL_HOST_PASSWORD in settings.py with a real App Password. For now, use the OTP below.)"
                print("\n" + "="*50)
                print(f"[{timezone.now()}] OTP FOR {email}: {code}")
                print("="*50 + "\n")
            else:
                subject = 'Your Password Reset OTP'
                message = f'Your One-Time Password (OTP) for password reset is: {code}\n\nThis OTP is valid for 5 minutes.'
                actual_email = getattr(settings, 'EMAIL_HOST_USER', 'noreply@example.com')
                email_from = actual_email 
                recipient_list = [email]
                
                send_mail(subject, message, email_from, recipient_list, fail_silently=False)
                print(f"OTP email sent to {email}: {code}")
                
        except Exception as e:
            setup_warning = f" (NOTE: Email failed. Error code: {str(e)[:20]})"
            print(f"\n[{timezone.now()}] ERROR SENDING OTP TO {email}: {str(e)}\n")

        # For the prototype, we include the code in the response to make testing easier 
        # for the user if they can't set up the email server.
        # IN PRODUCTION: Remove "code" from this JSON response!
        msg = f"OTP sent to {email}"
        if setup_warning:
            msg = f"OTP generated. {setup_warning}"

        return Response({
            "message": msg,
            "code": code 
        })

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        
        if not email or not code:
            return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        otp_obj = OTP.objects.filter(email=email, code=code).order_by('-created_at').first()
        
        if otp_obj:
            # Check if expired (e.g., 5 minutes)
            if otp_obj.created_at < timezone.now() - datetime.timedelta(minutes=5):
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
                
            otp_obj.is_verified = True
            otp_obj.save()
            return Response({"message": "OTP verified successfully"})
            
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def forgot_password(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
        # For the prototype, we just return a success message if the email exists.
        # In a real app, this would generate a token and send an email or OTP.
        if User.objects.filter(email=email).exists():
            return Response({"message": "Password reset link/OTP sent to your email"}, status=status.HTTP_200_OK)
        else:
            # For security, standard practice is to return success even if not found to prevent email enumeration,
            # but for this prototype, we'll return an error if it doesn't exist just to help testing.
            return Response({"error": "No user found with this email"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def reset_password(self, request):
        """
        Endpoint for ResetPasswordActivity.
        Expects email, new_password, and confirm_password.
        """
        email = request.data.get("email")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not new_password or not confirm_password:
            return Response({"error": "Both password fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        # In a real app we'd verify an OTP / token here.
        # For the prototype, we'll reset if the email exists.
        # If email is not provided, we might be resetting the currently logged in user (e.g. from Profile Settings).
        
        user_id = request.data.get("user_id")
        user = None
        
        if email:
            user = User.objects.filter(email=email).first()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
        else:
            return Response({"error": "Email or user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            user.set_password(new_password)
            user.save()
            return Response({"status": "Password updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get', 'put'])
    def profile(self, request):
        """
        Endpoint to handle GET and PUT for user profile data (activity_profile_settings.xml).
        In a real app, this would use request.user. For the prototype, we'll
        fetch the first user or accept a user_id parameter.
        """
        user_id = request.query_params.get('user_id') or request.data.get('user_id')
        user = User.objects.filter(id=user_id).first() if user_id else User.objects.first()
        
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
        profile = getattr(user, 'profile', None)
        
        if request.method == 'GET':
            data = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": f"{user.first_name} {user.last_name}".strip() or user.username,
                "email": user.email,
                "role": profile.get_role_display() if profile else "Unknown",
                "department": profile.department if profile else "",
                "phone_number": profile.phone_number if profile else "",
                "employee_id": profile.employee_id if profile else ""
            }
            return Response(data)
            
        elif request.method == 'PUT':
            # Update User fields
            if 'full_name' in request.data:
                names = request.data['full_name'].split(' ', 1)
                user.first_name = names[0]
                if len(names) > 1:
                    user.last_name = names[1]
                else:
                    user.last_name = ""
            if 'email' in request.data:
                user.email = request.data['email']
            user.save()
            
            # Update Profile fields
            if profile:
                if 'department' in request.data:
                    profile.department = request.data['department']
                if 'phone_number' in request.data:
                    profile.phone_number = request.data['phone_number']
                if 'employee_id' in request.data:
                    profile.employee_id = request.data['employee_id']
                profile.save()
                
            return Response({"status": "Profile updated successfully"})

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def perform_create(self, serializer):
        patient = serializer.save()
        # Notify Admin
        admin = User.objects.filter(profile__role='adminastrator').first()
        recorded_by = self.request.user if self.request.user.is_authenticated else User.objects.first()
        if admin:
            Notification.objects.create(
                user=admin,
                title="New Patient Added",
                message=f"{recorded_by.first_name or recorded_by.username} added patient: {patient.full_name}"
            )

    def perform_update(self, serializer):
        patient = serializer.save()
        # Notify Admin
        admin = User.objects.filter(profile__role='adminastrator').first()
        recorded_by = self.request.user if self.request.user.is_authenticated else User.objects.first()
        if admin:
            Notification.objects.create(
                user=admin,
                title="Patient Details Updated",
                message=f"{recorded_by.first_name or recorded_by.username} updated details for: {patient.full_name}"
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        patient_name = instance.full_name
        user = request.user if request.user.is_authenticated else None
        
        # Perform deletion
        response = super().destroy(request, *args, **kwargs)
        
        # Notify Administrators
        admins = User.objects.filter(profile__role='adminastrator')
        actor_name = "Someone"
        if user:
             actor_name = f"{user.first_name} {user.last_name}".strip() or user.username
        
        for admin in admins:
            Notification.objects.create(
                user=admin,
                title="Patient Record Deleted",
                message=f"{actor_name} permanently deleted the record for patient {patient_name}."
            )
            
        # Global Audit Log
        AuditLog.objects.create(
            user=user,
            action="Deleted Patient Record",
            details=f"Patient {patient_name}",
            icon_type="warning"
        )
        
        return response

    @action(detail=False, methods=['get'])
    def monitor_list(self, request):
        """
        Endpoint to feed activity_monitor.xml (Live Monitor List)
        """
        patients = self.get_queryset()
        
        # Calculate status counts based on active alerts
        # For prototype, we'll infer status:
        # Critical = has Critical alert
        # Warning = has Warning alert
        # Normal = no active alerts
        
        patient_list_data = []
        normal_count = 0
        warning_count = 0
        critical_count = 0
        
        for patient in patients:
            active_alerts = patient.alerts.filter(status='Active')
            
            if active_alerts.filter(alert_type='Critical').exists():
                status_calc = 'Critical'
                critical_count += 1
            elif active_alerts.filter(alert_type='Warning').exists():
                status_calc = 'Warning'
                warning_count += 1
            else:
                status_calc = 'Normal'
                normal_count += 1
                
            # Get latest vitals
            latest_vitals = patient.vitals.order_by('-timestamp').first()
            
            vitals_dict = {
                "tv": None,
                "rr": None,
                "fio2": None,
                "spo2": None
            }
            
            if latest_vitals:
                vitals_dict['tv'] = latest_vitals.vte
                vitals_dict['rr'] = latest_vitals.respiratory_rate
                vitals_dict['fio2'] = latest_vitals.fio2
                vitals_dict['spo2'] = latest_vitals.spo2
                
            patient_list_data.append({
                "id": patient.id,
                "name": patient.full_name,
                "bed_number": patient.bed_number,
                "status": status_calc,
                "vitals": vitals_dict
            })
            
        return Response({
            "status_counts": {
                "active": normal_count,
                "warning": warning_count,
                "critical": critical_count
            },
            "patients": patient_list_data
        })

    @action(detail=True, methods=['get'])
    def monitor_data(self, request, pk=None):
        """
        Endpoint specifically designed to feed activity_monitor_bed.xml
        """
        patient = self.get_object()
        
        # Get latest vitals
        latest_vitals = patient.vitals.order_by('-timestamp').first()
        vitals_data = VitalSignSerializer(latest_vitals).data if latest_vitals else None
        
        # Get active device status
        device = patient.device
        device_data = None
        if device:
            device_data = {
                "type": device.device_type,
                "status": device.status,
                "connection": "Connected" if device.status == "Active" else "Disconnected"
            }
        return Response({
            "patient_info": {
                "name": patient.full_name,
                "bed_number": patient.bed_number,
                "status": patient.status
            },
            "device": device_data,
            "current_vitals": vitals_data
        })

    @action(detail=False, methods=['get'])
    def patients_list(self, request):
        """
        Endpoint for Patients List Screen (activity_patients.xml)
        Supports filtering by status (Critical, Stable, Warning)
        """
        patients = self.get_queryset()
        
        status_filter = request.query_params.get('status_filter') # 'All', 'Critical', 'Stable', 'Warning'
        
        patient_list_data = []
        for patient in patients:
            active_alerts = patient.alerts.filter(status='Active')
            
            if active_alerts.filter(alert_type='Critical').exists():
                status_calc = 'Critical'
            elif active_alerts.filter(alert_type='Warning').exists():
                status_calc = 'Warning'
            else:
                status_calc = 'Normal'
                
            # Convert dob to mock age for prototype
            age = "65y" # Mocked
            if patient.dob and len(patient.dob) > 4:
                try: # Very basic mock extraction if it was a year
                    age = str(2023 - int(patient.dob[-4:])) + "y"
                except: pass
                
            if status_filter and status_filter != 'All':
                target_status = 'Normal' if status_filter == 'Stable' else status_filter
                if status_calc != target_status:
                    continue

            patient_list_data.append({
                "id": patient.id,
                "full_name": patient.full_name,
                "name": patient.full_name,
                "patient_id": patient.patient_id,
                "idNum": patient.patient_id,
                "age": age,
                "gender": patient.gender,
                "bed_number": patient.bed_number,
                "bed": patient.bed_number,
                "status": status_calc if status_calc != 'Normal' else (patient.status if patient.status != 'Admitted' else 'Stable'),
                "diagnosis": patient.primary_diagnosis,
                "condition": patient.primary_diagnosis or "Unknown",
                "admission_date": patient.admission_date,
                "admitted": patient.admission_date,
                "attending_physician": patient.attending_physician,
                "physician": patient.attending_physician,
                "formatted_details": f"ID: {patient.patient_id} • {age}",
                "formatted_bed": f"Bed: {patient.bed_number}",
            })
            
        return Response(patient_list_data)

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """
        Endpoint for Patient Details Screen (activity_patient_details.xml)
        """
        patient = self.get_object()
        
        # Base Patient Info
        patient_data = PatientSerializer(patient).data
        # Augment with Age (from DOB simplified)
        patient_data['age_display'] = "65y" # Mocked for prototype based on UI
        
        # Latest Vitals
        latest_vitals = patient.vitals.order_by('-timestamp').first()
        vitals_data = VitalSignSerializer(latest_vitals).data if latest_vitals else None
        
        # Active Device & Settings
        device = patient.device
        device_data = None
        if device:
            # The device.current_settings JSONField would normally hold these
            # For the prototype, we'll mock them if the device is a Vent to match UI
            device_data = {
                "type": device.device_type,
                "status": device.status,
                "mode": device.current_settings.get('mode', 'AC/VC Mode'),
                "peep": device.current_settings.get('peep', '8.0'),
                "fio2": device.current_settings.get('fio2', '60%'),
                "rr": device.current_settings.get('rr', '24'),
            }
            
        # AI Risk Assessment
        latest_risk = patient.risk_assessments.order_by('-timestamp').first()
        risk_data = None
        if latest_risk:
            risk_data = {
                "score": latest_risk.risk_score,
                "status": "High Risk Patient" if latest_risk.risk_score > 75 else "Stable"
            }
            
        return Response({
            "patient": patient_data,
            "vitals": vitals_data,
            "device_settings": device_data,
            "risk_assessment": risk_data
        })

class PatientHistoryViewSet(viewsets.ModelViewSet):
    queryset = PatientHistory.objects.all()
    serializer_class = PatientHistorySerializer

    def get_queryset(self):
        queryset = PatientHistory.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset.order_by('-timestamp')

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    @action(detail=True, methods=['post'])
    def update_settings(self, request, pk=None):
        device = self.get_object()
        # The Android UI sends parameters like tidal_volume, peep, etc.
        # We'll merge them into the current_settings JSON field.
        new_settings = request.data
        
        device.current_settings.update(new_settings)
        device.save()

        # Notify Admin
        if device.assigned_patient:
            admin = User.objects.filter(profile__role='adminastrator').first()
            recorded_by = request.user if request.user.is_authenticated else User.objects.first()
            setting_name = list(new_settings.keys())[0] if new_settings else "settings"
            if admin:
                Notification.objects.create(
                    user=admin,
                    title="Ventilator Settings Changed",
                    message=f"{recorded_by.first_name or recorded_by.username} changed {setting_name} for {device.assigned_patient.full_name}"
                )
        
        # Log to PatientHistory as per UI requirement ("All changes are logged")
        if device.assigned_patient:
            setting_str = ", ".join([f"{k}: {v}" for k, v in new_settings.items()])
            PatientHistory.objects.create(
                patient=device.assigned_patient,
                event_type='treatment',
                event_title='Ventilator Settings Updated',
                event_description=f"Clinical adjustments: {setting_str}",
                recorded_by=request.user if request.user.is_authenticated else User.objects.first()
            )
            
            # Global Audit Log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else User.objects.first(),
                action="Changed Ventilator Settings",
                details=f"Patient {device.assigned_patient.full_name}",
                icon_type="system"
            )
            
        return Response({
            "status": "Settings updated successfully", 
            "current_settings": device.current_settings
        })

class VitalSignViewSet(viewsets.ModelViewSet):
    queryset = VitalSign.objects.all()
    serializer_class = VitalSignSerializer
    
    def get_queryset(self):
        queryset = VitalSign.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        time_range = self.request.query_params.get('time_range')
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
            
        if time_range:
            now = timezone.now()
            if time_range == '4h':
                queryset = queryset.filter(timestamp__gte=now - datetime.timedelta(hours=4))
            elif time_range == '12h':
                queryset = queryset.filter(timestamp__gte=now - datetime.timedelta(hours=12))
            elif time_range == '24h':
                queryset = queryset.filter(timestamp__gte=now - datetime.timedelta(hours=24))
            elif time_range == '7d':
                queryset = queryset.filter(timestamp__gte=now - datetime.timedelta(days=7))
                
        return queryset.order_by('-timestamp')

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = Alert.objects.all()
        alert_type = self.request.query_params.get('alert_type')
        patient_id = self.request.query_params.get('patient_id')
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if alert_type and alert_type != 'All':
            queryset = queryset.filter(alert_type=alert_type)
            
        return queryset.order_by('-timestamp')

    @action(detail=True, methods=['put'])
    def acknowledge(self, request, pk=None):
        alert = self.get_object()
        alert.status = "Acknowledged"
        alert.save()
        return Response({"status": "Alert acknowledged"})

    @action(detail=True, methods=['post'])
    def escalate(self, request, pk=None):
        alert = self.get_object()
        staff_id = request.data.get('staff_id')
        if staff_id:
            try:
                staff_user = User.objects.get(id=staff_id)
                alert.escalated_to = staff_user
            except User.DoesNotExist:
                return Response({"error": "Staff not found"}, status=status.HTTP_404_NOT_FOUND)
                
        alert.status = "Escalated"
        alert.save()
        
        response_data = {"status": "Alert escalated"}
        if alert.escalated_to:
            response_data["escalated_to"] = alert.escalated_to.username
            
        return Response(response_data)

    @action(detail=True, methods=['post'])
    def silence(self, request, pk=None):
        alert = self.get_object()
        # In a real app, this would start a 2-minute timer on the backend
        # For the prototype, we just mark it as silenced and record the time
        alert.status = "Silenced"
        alert.save()
        return Response({
            "status": "Alert silenced for 2 minutes",
            "alert_id": alert.id
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - datetime.timedelta(days=7)
        
        patient_id = request.query_params.get('patient_id')
        queryset = self.get_queryset()
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
            
        active_count = queryset.filter(status='Active').count()
        today_count = queryset.filter(timestamp__gte=today).count()
        week_count = queryset.filter(timestamp__gte=week_ago).count()
        
        critical_count = queryset.filter(alert_type='Critical').count()
        warning_count = queryset.filter(alert_type='Warning').count()
        info_count = queryset.filter(alert_type='Info').count()
        
        return Response({
            "active_alerts": active_count,
            "alerts_today": today_count,
            "alerts_week": week_count,
            "distribution": {
                "critical": critical_count,
                "warning": warning_count,
                "info": info_count
            }
        })

    @action(detail=False, methods=['get'])
    def ai_summary(self, request):
        """
        Consolidated AI stats for activity_smart_alarm_ai.xml
        """
        queryset = self.get_queryset()
        total_alarms = queryset.count()
        # Mock logic based on UI stats
        false_filtered = queryset.filter(status='Silenced').count() or total_alarms // 2
        true_positives = queryset.filter(alert_type='Critical', status='Acknowledged').count() or total_alarms // 3
        accuracy = "94.2%"
        fatigue_reduction = "57%"
        
        classification = {
            "true_critical": 25,
            "true_warning": 45,
            "false_positive": 20,
            "noise": 10
        }
        
        return Response({
            "total_alarms": total_alarms,
            "false_filtered": false_filtered,
            "true_positives": true_positives,
            "accuracy": accuracy,
            "fatigue_reduction": fatigue_reduction,
            "classification": classification
        })

    @action(detail=False, methods=['get'])
    def recent_decisions(self, request):
        """
        Recent AI Decisions list for activity_smart_alarm_ai.xml
        """
        queryset = self.get_queryset().order_by('-timestamp')[:5]
        data = []
        for alert in queryset:
            data.append({
                "id": alert.id,
                "event": alert.description[:20],
                "outcome": "True Positive" if alert.alert_type == 'Critical' else "False Alarm",
                "confidence": f"{alert.ai_confidence or 92}%",
                "timestamp_display": "2m ago" # Mocked for simplicity
            })
        return Response(data)

class AIPredictedEventViewSet(viewsets.ModelViewSet):
    queryset = AIPredictedEvent.objects.all()
    serializer_class = AIPredictedEventSerializer

    def get_queryset(self):
        queryset = AIPredictedEvent.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def get_queryset(self):
        queryset = Report.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset.order_by('-uploaded_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        
        # Enhance data for the UI (activity_reports_and_documents.xml & list_item_report.xml)
        enhanced_data = []
        for item in serializer.data:
            # Format size (e.g., 1200000 -> "1.2 MB")
            size_bytes = item.get('file_size_bytes', 0)
            if size_bytes > 1024 * 1024:
                size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
            elif size_bytes > 1024:
                size_str = f"{size_bytes / 1024:.1f} KB"
            else:
                size_str = f"{size_bytes} B"
                
            # Format date (e.g., "Oct 14, 2023")
            uploaded_at_str = item.get('uploaded_at')
            date_str = ""
            if uploaded_at_str:
                try:
                    dt = parse(uploaded_at_str)
                    date_str = dt.strftime("%b %d, %Y")
                except:
                    date_str = uploaded_at_str[:10]
            
            # Match the UI string "Oct 14, 2023  •  1.2 MB"
            report_details = f"{date_str}  •  {size_str}"
            
            item['report_details'] = report_details
            enhanced_data.append(item)
            
        return Response(enhanced_data)

from .models import AIChatMessage
from .serializers import AIChatMessageSerializer

class AIChatMessageViewSet(viewsets.ModelViewSet):
    queryset = AIChatMessage.objects.all()
    serializer_class = AIChatMessageSerializer

    def get_queryset(self):
        queryset = AIChatMessage.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        return queryset.order_by('timestamp')

    @action(detail=False, methods=['post'])
    def chat(self, request):
        patient_id = request.data.get('patient_id')
        message_text = request.data.get('message')
        
        patient = Patient.objects.filter(id=patient_id).first() if patient_id else None
        
        # Save user message
        user_msg = AIChatMessage.objects.create(
            patient=patient,
            sender='user',
            message=message_text
        )
        
        # Smarter AI Logic for VentGuard Prototype
        text_lower = message_text.lower()
        
        confidence = 85
        causes = []
        actions = []
        
        if "pressure" in text_lower or "pip" in text_lower:
            ai_response_text = "High peak pressure detected. This often indicates increased airway resistance or decreased lung compliance."
            confidence = 92
            causes = [
                {"cause": "Secretions/Mucus Plug", "probability": "85%"},
                {"cause": "Patient Agitation/Coughing", "probability": "70%"},
                {"cause": "Tube Kinking", "probability": "60%"}
            ]
            actions = [
                "Suction the airway to clear secretions",
                "Check sedation levels (RASS score)",
                "Verify ETT (Endotracheal Tube) positioning"
            ]
        elif "peep" in text_lower:
            ai_response_text = "I recommend maintaining current PEEP at 8.0 cmH2O. Increasing PEEP may exacerbate the peak pressure issue without improving oxygenation given the current compliance."
            confidence = 88
            causes = []
            actions = [
                "Monitor oxygenation (SpO2)",
                "Consider lung recruitment maneuver if PaO2 drops"
            ]
        elif "volume" in text_lower or "tidal" in text_lower or "vte" in text_lower:
            ai_response_text = "Low tidal volume observed. This could be due to a leak in the circuit or sudden changes in patient lung conditions."
            confidence = 89
            causes = [
                {"cause": "Circuit Leak", "probability": "80%"},
                {"cause": "Cuff Deflation", "probability": "65%"},
                {"cause": "Worsening Compliance", "probability": "50%"}
            ]
            actions = [
                "Check ventilator circuit for obvious leaks",
                "Check ETT cuff pressure",
                "Review pressure-volume loops"
            ]
        elif "oxygen" in text_lower or "spo2" in text_lower or "fio2" in text_lower:
            ai_response_text = "Desaturation noted. Before increasing FiO2, consider checking airway patency."
            confidence = 94
            causes = [
                {"cause": "Mucus Plugging", "probability": "75%"},
                {"cause": "Loss of PEEP", "probability": "60%"},
                {"cause": "Ventilator Asynchrony", "probability": "55%"}
            ]
            actions = [
                "Briefly increase FiO2 to 100% (100% O2 suction mode)",
                "Suction patient if secretions suspected",
                "Assess for signs of pneumothorax if sudden"
            ]
        elif "rate" in text_lower or "rr" in text_lower or "breath" in text_lower:
            ai_response_text = "High respiratory rate (tachypnea) detected. This may indicate patient distress or pain."
            confidence = 82
            causes = [
                {"cause": "Pain/Agitation", "probability": "80%"},
                {"cause": "Hypoxia or Hypercapnia", "probability": "75%"},
                {"cause": "Fever/Sepsis", "probability": "40%"}
            ]
            actions = [
                "Evaluate patient for pain and administer analgesia if needed",
                "Check recent ABG results",
                "Examine flow-time curve for double-triggering or auto-PEEP"
            ]
        else:
            ai_response_text = "Based on the input and current ventilator parameters, the patient appears relatively stable, but continuous monitoring is advised. Could you provide more specific symptoms or parameters (like pressure, volume, or SpO2)?"
            confidence = 75

        # Save AI message
        ai_msg = AIChatMessage.objects.create(
            patient=patient,
            sender='ai',
            message=ai_response_text,
            confidence_score=confidence,
            likely_causes=causes,
            recommended_actions=actions
        )
        
        return Response({
            "user_message": AIChatMessageSerializer(user_msg).data,
            "ai_response": AIChatMessageSerializer(ai_msg).data
        }, status=status.HTTP_201_CREATED)

from .models import PatientRisk
from .serializers import PatientRiskSerializer

class PatientRiskViewSet(viewsets.ModelViewSet):
    queryset = PatientRisk.objects.all()
    serializer_class = PatientRiskSerializer

    def get_queryset(self):
        queryset = PatientRisk.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        # Order by highest risk first by default
        return queryset.order_by('-risk_score')

from .models import AlertSetting
from .serializers import AlertSettingSerializer

class AlertSettingViewSet(viewsets.ModelViewSet):
    queryset = AlertSetting.objects.all()
    serializer_class = AlertSettingSerializer

    def get_queryset(self):
        queryset = AlertSetting.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

from .models import Anomaly
from .serializers import AnomalySerializer

class AnomalyViewSet(viewsets.ModelViewSet):
    queryset = Anomaly.objects.all()
    serializer_class = AnomalySerializer

    def get_queryset(self):
        queryset = Anomaly.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        is_reviewed = self.request.query_params.get('is_reviewed')
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if is_reviewed is not None:
            # Convert string to boolean
            is_reviewed = is_reviewed.lower() in ['true', '1']
            queryset = queryset.filter(is_reviewed=is_reviewed)
            
        return queryset.order_by('-timestamp')

    @action(detail=False, methods=['post'])
    def mark_all_reviewed(self, request):
        patient_id = request.data.get('patient_id')
        queryset = Anomaly.objects.filter(is_reviewed=False)
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
            
        updated_count = queryset.update(is_reviewed=True)
        return Response({"status": "Success", "updated_count": updated_count})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        
        now = timezone.now()
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        patient_id = request.query_params.get('patient_id')
        queryset = self.get_queryset()
        
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
            
        detected_today = queryset.filter(timestamp__gte=today).count()
        # Mocking the patterns learned and accuracy for the UI
        patterns_learned = "2.8K" 
        accuracy = "96%"
        
        return Response({
            "detected_today": detected_today,
            "patterns_learned": patterns_learned,
            "accuracy": accuracy
        })

from .models import AppearanceSetting
from .serializers import AppearanceSettingSerializer

class AppearanceSettingViewSet(viewsets.ModelViewSet):
    queryset = AppearanceSetting.objects.all()
    serializer_class = AppearanceSettingSerializer

    def get_queryset(self):
        queryset = AppearanceSetting.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class StaffViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(profile__isnull=False)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.filter(profile__isnull=False)
        role = self.request.query_params.get('role')
        if role:
            queryset = queryset.filter(profile__role=role)
        return queryset

from .models import FAQ, SupportTicket
from .serializers import FAQSerializer, SupportTicketSerializer

class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQSerializer

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

    def get_queryset(self):
        queryset = SupportTicket.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        # Default to the first user if none provided for prototype
        user = self.request.user if self.request.user.is_authenticated else User.objects.first()
        serializer.save(user=user)

class DashboardViewSet(viewsets.ViewSet):
    """
    Aggregation endpoint for Home screen (activity_home.xml)
    """
    def list(self, request):
        from .models import Patient, Device, Alert, Profile, AIPredictedEvent, PatientRisk, Anomaly
        
        # Stats (Raw counts for real-time accuracy)
        active_patients = Patient.objects.count()
        active_vents = Patient.objects.filter(bed_number__icontains="ICU").count()
        active_alerts = Alert.objects.filter(status="Active").count()
        staff_online = Profile.objects.count()

        # AI Insights
        predictive_alerts_count = AIPredictedEvent.objects.count()
        high_risk_patients_count = PatientRisk.objects.filter(risk_score__gte=80).count()
        
        # Recent Alerts
        recent_alerts = Alert.objects.filter(status="Active").order_by('-timestamp')[:4]
        from .serializers import AlertSerializer
        recent_alerts_data = AlertSerializer(recent_alerts, many=True).data

        return Response({
            "stats": {
                "active_patients": active_patients,
                "active_vents": active_vents,
                "active_alerts": active_alerts,
                "staff_online": staff_online
            },
            "ai_insights": {
                "predictive_alerts": predictive_alerts_count,
                "false_alarm_rate": "57%", # Mock value as per layout
                "high_risk_patients": high_risk_patients_count
            },
            "recent_alerts": recent_alerts_data
        })

from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = Notification.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-created_at')

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        user_id = request.data.get('user_id')
        queryset = Notification.objects.filter(is_read=False)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        updated_count = queryset.update(is_read=True)
        return Response({"status": "Success", "updated_count": updated_count})

class SecuritySettingViewSet(viewsets.ModelViewSet):
    queryset = SecuritySetting.objects.all()
    serializer_class = SecuritySettingSerializer

    def get_queryset(self):
        queryset = SecuritySetting.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoginHistory.objects.all()
    serializer_class = LoginHistorySerializer

    def get_queryset(self):
        queryset = LoginHistory.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset.order_by('-login_time')

class OnboardingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OnboardingStep.objects.all().order_by('order')
    serializer_class = OnboardingStepSerializer

class MetadataViewSet(viewsets.ViewSet):
    """
    Returns constant lists for populating Spinners/Dropdowns in the UI (spinner_item_layout.xml)
    """
    def list(self, request):
        return Response({
            "roles": ["Doctor", "Nurse", "Respiratory Therapist", "Administrator"],
            "departments": ["ICU-01", "ICU-02", "Emergency", "Cardiology", "Neurology"],
            "alert_types": ["All", "Critical", "Warning", "Info"],
            "genders": ["Male", "Female", "Other"],
            "patient_statuses": ["Stabilized", "Critical", "Observation", "Ready for Discharge"]
        })

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all().order_by('-timestamp')
    serializer_class = AuditLogSerializer

class UserManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def check_admin(self, request):
        if not hasattr(request.user, 'profile') or request.user.profile.role != 'adminastrator':
            raise PermissionDenied("Only administrators can perform this action.")

    @action(detail=False, methods=['get'])
    def list_users(self, request):
        self.check_admin(request)
        
        users = User.objects.all().order_by('-date_joined')
        role_filter = request.query_params.get('role')
        if role_filter and role_filter != 'All':
            role_map = {
                "Doctors": "doctor",
                "Nurses": "nurse",
                "RTs": "respiratory_therapist",
                "Admins": "adminastrator"
            }
            backend_role = role_map.get(role_filter)
            if backend_role:
                users = users.filter(profile__role=backend_role)
        
        data = []
        for user in users:
            profile = getattr(user, 'profile', None)
            data.append({
                "id": user.id,
                "full_name": f"{user.first_name} {user.last_name}".strip() or user.username,
                "role": profile.role if profile else "Unknown",
                "role_display": profile.get_role_display() if profile else "Unknown",
                "department": profile.department if profile else "",
                "status": "Approved" if (profile and profile.is_approved) else "Pending",
                "is_approved": profile.is_approved if profile else False
            })
        return Response(data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        self.check_admin(request)
        try:
            target_user = User.objects.get(id=pk)
            profile = target_user.profile
            profile.is_approved = True
            profile.save()
            
            Notification.objects.create(
                user=target_user,
                title="Account Approved",
                message="Your account has been approved by the administrator. You can now access the dashboard."
            )
            
            # Mark signup notification as read
            Notification.objects.filter(
                target_user_id=pk, 
                title="New User Signup"
            ).update(is_read=True)
            
            # Global Audit Log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                system_actor="System" if not request.user.is_authenticated else None,
                action="Approved User",
                details=target_user.username,
                icon_type="user"
            )
            
            return Response({"status": "User approved successfully"})
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Response({"error": "User not found"}, status=404)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        self.check_admin(request)
        try:
            target_user = User.objects.get(id=pk)
            profile = target_user.profile
            profile.is_approved = False
            profile.save()
            
            return Response({"status": "User deactivated successfully"})
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Response({"error": "User not found"}, status=404)

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        self.check_admin(request)
        try:
            target_user = User.objects.get(id=pk)
            # The profile is deleted automatically because of the models.CASCADE relationship on OneToOneField
            target_user.delete()
            return Response({"status": "User deleted successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    @action(detail=True, methods=['post'])
    def make_admin(self, request, pk=None):
        self.check_admin(request)
        try:
            target_user = User.objects.get(id=pk)
            profile = target_user.profile
            profile.role = 'adminastrator'
            profile.is_approved = True
            profile.save()
            
            # Global Audit Log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                system_actor="System" if not request.user.is_authenticated else None,
                action="Promoted to Admin",
                details=target_user.username,
                icon_type="admin"
            )
            
            return Response({"status": "User promoted to Admin successfully"})
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Response({"error": "User not found"}, status=404)

    @action(detail=True, methods=['post'])
    def dismiss_admin(self, request, pk=None):
        self.check_admin(request)
        try:
            target_user = User.objects.get(id=pk)
            # Prevent demoting yourself
            if target_user == request.user:
                return Response({"error": "You cannot demote yourself from Admin status."}, status=400)
                
            profile = target_user.profile
            profile.role = 'doctor' # Default role after dismissal
            profile.save()
            
            # Global Audit Log
            AuditLog.objects.create(
                user=request.user if request.user.is_authenticated else None,
                system_actor="System" if not request.user.is_authenticated else None,
                action="Dismissed Admin",
                details=target_user.username,
                icon_type="warning"
            )
            
            return Response({"status": "User dismissed as Admin successfully"})
        except (User.DoesNotExist, Profile.DoesNotExist):
            return Response({"error": "User not found"}, status=404)
