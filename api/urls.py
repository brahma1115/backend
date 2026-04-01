from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from .views import (AuthViewSet, PatientViewSet, PatientHistoryViewSet, DeviceViewSet, 
                    VitalSignViewSet, AlertViewSet, AIPredictedEventViewSet, ReportViewSet, 
                    AIChatMessageViewSet, PatientRiskViewSet, AlertSettingViewSet,
                    AnomalyViewSet, AppearanceSettingViewSet, StaffViewSet,
                    FAQViewSet, SupportTicketViewSet, DashboardViewSet, NotificationViewSet,
                    SecuritySettingViewSet, LoginHistoryViewSet, OnboardingViewSet, MetadataViewSet,
                    UserManagementViewSet, AuditLogViewSet)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'user-management', UserManagementViewSet, basename='user-management')
router.register(r'patient-history', PatientHistoryViewSet, basename='patient-history')
router.register(r'monitoring/beds', DeviceViewSet, basename='devices')
router.register(r'monitoring/vitals', VitalSignViewSet, basename='vitals')
router.register(r'alerts', AlertViewSet, basename='alerts')
router.register(r'ai/predictions', AIPredictedEventViewSet, basename='ai-predictions')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'ai-assistant-chat', AIChatMessageViewSet, basename='ai-assistant-chat')
router.register(r'risk-assessment', PatientRiskViewSet, basename='risk-assessment')
router.register(r'alert-settings', AlertSettingViewSet, basename='alert-settings')
router.register(r'anomalies', AnomalyViewSet, basename='anomalies')
router.register(r'appearance-settings', AppearanceSettingViewSet, basename='appearance-settings')
router.register(r'staff', StaffViewSet, basename='staff')
router.register(r'faqs', FAQViewSet, basename='faqs')
router.register(r'support-tickets', SupportTicketViewSet, basename='support-tickets')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'security-settings', SecuritySettingViewSet, basename='security-settings')
router.register(r'login-history', LoginHistoryViewSet, basename='login-history')
router.register(r'onboarding', OnboardingViewSet, basename='onboarding')
router.register(r'metadata', MetadataViewSet, basename='metadata')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-logs')

urlpatterns = [
    path('login/', csrf_exempt(AuthViewSet.as_view({'post': 'login'})), name='api-login'),
    path('register/', csrf_exempt(AuthViewSet.as_view({'post': 'register'})), name='api-register'),
    path('forgot-password/', csrf_exempt(AuthViewSet.as_view({'post': 'forgot_password'})), name='api-forgot-password'),
    path('reset-password/', csrf_exempt(AuthViewSet.as_view({'post': 'reset_password'})), name='api-reset-password'),
    path('send-otp/', csrf_exempt(AuthViewSet.as_view({'post': 'send_otp'})), name='api-send-otp'),
    path('verify-otp/', csrf_exempt(AuthViewSet.as_view({'post': 'verify_otp'})), name='api-verify-otp'),
    path('login/delete_account/', csrf_exempt(AuthViewSet.as_view({'delete': 'delete_account'})), name='api-delete-account'),
    path('profile/', csrf_exempt(AuthViewSet.as_view({'get': 'profile', 'put': 'profile'})), name='api-profile'),
    path('', include(router.urls)),
]
