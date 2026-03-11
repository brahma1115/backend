import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/"

def test_alerts_filtering():
    print("\n--- Testing Alerts Filtering ---")
    # All alerts
    resp = requests.get(f"{BASE_URL}alerts/")
    print(f"All Alerts Status: {resp.status_code}, Count: {len(resp.json())}")
    
    # Critical only
    resp = requests.get(f"{BASE_URL}alerts/?alert_type=Critical")
    print(f"Critical Alerts Status: {resp.status_code}, Count: {len(resp.json())}")
    for alert in resp.json():
        print(f"- {alert['alert_type']}: {alert['description']} ({alert['patient_name']})")

def test_patient_history():
    print("\n--- Testing Patient History Timeline ---")
    resp = requests.get(f"{BASE_URL}patient-history/")
    print(f"History Status: {resp.status_code}, Count: {len(resp.json())}")
    for item in resp.json():
        print(f"[{item['timestamp_display']}] {item['event_title']}: {item['event_description']}")

def test_vitals_history():
    print("\n--- Testing Vitals History & MAP ---")
    # Get vitals
    resp = requests.get(f"{BASE_URL}monitoring/vitals/")
    print(f"Vitals List Status: {resp.status_code}")
    if resp.json():
        sample = resp.json()[0]
        print(f"Sample Vitals: Sys={sample.get('blood_pressure_sys')}, Dia={sample.get('blood_pressure_dia')}, MAP={sample.get('mean_arterial_pressure')}")
    
    # Test time range
    for r in ['4h', '24h', '7d']:
        resp = requests.get(f"{BASE_URL}monitoring/vitals/?time_range={r}")
        print(f"Range {r} Status: {resp.status_code}, Count: {len(resp.json())}")

def test_risk_assessments():
    print("\n--- Testing Patient Risk Assessments ---")
    resp = requests.get(f"{BASE_URL}risk-assessment/")
    print(f"Risk Assessments Status: {resp.status_code}, Count: {len(resp.json())}")
    for risk in resp.json():
        print(f"- Risk Score: {risk['risk_score']} for {risk['patient_name']} (Bed: {risk['bed_number']})")
        print(f"  Factors: {', '.join(risk['risk_factors'])}")

if __name__ == "__main__":
    try:
        test_alerts_filtering()
        test_vitals_history()
        test_risk_assessments()
        test_patient_history()
    except Exception as e:
        print(f"Connection error: {e}. Make sure the server is running!")
