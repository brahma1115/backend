from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token 
from .models import (Profile, Patient, PatientHistory, Device, VitalSign, Alert, 
                     AIPredictedEvent, Report, SecuritySetting, LoginHistory, OnboardingStep, OTP) 
from .serializers import (UserSerializer, PatientSerializer, PatientHistorySerializer, 
                          DeviceSerializer, VitalSignSerializer, AlertSerializer, 
                          AIPredictedEventSerializer, ReportSerializer, 
                          SecuritySettingSerializer, LoginHistorySerializer, OnboardingStepSerializer, OTPSerializer)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):

        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        # login using email
        if email:
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials"}, status=401)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": UserSerializer(user).data
            })

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['post'])
    def register(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password")
        full_name = request.data.get("full_name", "")
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
            "Nurse": "nurse",
            "Respiratory Therapist": "respiratory_therapist",
            "Administrator": "adminastrator" 
        }
        
        backend_role = role_map.get(role, role.lower().replace(" ", "_"))

        Profile.objects.create(user=user, role=backend_role)
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            "message": "User created successfully",
            "token": token.key, 
            "user": UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def send_otp(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # In a real app, generate a random 6-digit code and send via email
        # For prototype, we'll use a fixed code or random and return it for testing
        import random
        code = str(random.randint(100000, 999999))
        
        OTP.objects.create(email=email, code=code)
        
        # Mocking email send
        print(f"OTP for {email}: {code}")
        
        return Response({
            "message": f"OTP sent to {email}",
            "code": code # In production, DO NOT return the code in the response
        })

    @action(detail=False, methods=['post'])
    def verify_otp(self, request):
        email = request.data.get("email")
        code = request.data.get("code")
        
        if not email or not code:
            return Response({"error": "Email and code are required"}, status=status.HTTP_400_BAD_REQUEST)
            
        otp_obj = OTP.objects.filter(email=email, code=code).order_by('-created_at').first()
        
        if otp_obj:
            from django.utils import timezone
            import datetime
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
                if status_filter == 'Stable' and status_calc != 'Normal':
                    continue
                if status_filter != 'Stable' and status_calc != status_filter:
                    continue

            patient_list_data.append({
                "id": patient.id,
                "name": patient.full_name,
                "patient_id": patient.patient_id,
                "age": age,
                "bed_number": patient.bed_number,
                "status": status_calc,
                "condition": patient.primary_diagnosis or "Unknown"
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
            from django.utils import timezone
            import datetime
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
        from django.utils import timezone
        import datetime
        
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
                from dateutil.parser import parse
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
        
        # Generate mock AI response based on the frontend layout
        ai_response_text = "Based on the patient's current waveform data and history, here is my analysis."
        if "peep" in message_text.lower():
            ai_response_text = "I recommend maintaining current PEEP at 8.0 cmH2O. Increasing PEEP may exacerbate the peak pressure issue."
            confidence = 92
            causes = []
            actions = []
        else:
            confidence = 85
            causes = [
                {"cause": "Secretions/Mucus Plug", "probability": "85%"},
                {"cause": "Patient Agitation", "probability": "60%"},
                {"cause": "Tube Kinking", "probability": "45%"}
            ]
            actions = [
                "Suction the airway to clear secretions",
                "Check sedation levels (RASS score)",
                "Verify tube positioning"
            ]

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
        from django.utils import timezone
        import datetime
        
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
    @action(detail=False, methods=['get'])
    def summary(self, request):
        from .models import Patient, Device, Alert, Profile, AIPredictedEvent, PatientRisk, Anomaly
        
        # Stats
        active_patients = Patient.objects.filter(status__icontains="Admit").count() or Patient.objects.count()
        active_vents = Device.objects.filter(status__icontains="Active", device_type__icontains="Vent").count() or Device.objects.count()
        active_alerts = Alert.objects.filter(status="Active").count()
        staff_online = Profile.objects.filter(role__in=['doctor', 'nurse', 'respiratory_therapist']).count() # Mock online

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
