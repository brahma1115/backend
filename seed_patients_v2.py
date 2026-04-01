import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from api.models import Patient, Alert, Device, VitalSign
from django.utils import timezone
import random

def get_vitals_by_diagnosis(diagnosis):
    """Returns realistic vitals and vent settings based on diagnosis."""
    vitals = {
        "heart_rate": random.randint(70, 90),
        "spo2": random.randint(96, 99),
        "respiratory_rate": random.randint(14, 18),
        "bp_sys": random.randint(115, 125),
        "bp_dia": random.randint(75, 85),
        "temp": random.uniform(36.6, 37.2),
        "tv": 450,
        "peep": 5.0,
        "fio2": 21,
        "mode": "AC/VC Mode"
    }

    if "ARDS" in diagnosis:
        vitals.update({
            "heart_rate": random.randint(95, 115),
            "spo2": random.randint(88, 92),
            "respiratory_rate": random.randint(22, 30),
            "peep": random.choice([10.0, 12.0, 14.0]),
            "fio2": random.choice([50, 60, 70]),
            "tv": random.randint(350, 420)
        })
    elif "Sepsis" in diagnosis:
        vitals.update({
            "heart_rate": random.randint(105, 130),
            "bp_sys": random.randint(85, 105),
            "bp_dia": random.randint(50, 65),
            "temp": random.uniform(38.5, 40.0),
            "peep": 8.0,
            "fio2": 40
        })
    elif "Heart Failure" in diagnosis:
        vitals.update({
            "heart_rate": random.randint(55, 75),
            "bp_sys": random.randint(95, 115),
            "spo2": random.randint(92, 95),
            "peep": 7.5,
            "fio2": 35
        })
    elif "Pneumonia" in diagnosis:
        vitals.update({
            "temp": random.uniform(38.0, 39.5),
            "spo2": random.randint(90, 94),
            "respiratory_rate": random.randint(20, 26),
            "fio2": 40
        })
    elif "Stroke" in diagnosis:
        vitals.update({
            "bp_sys": random.randint(150, 180),
            "bp_dia": random.randint(95, 110),
            "heart_rate": random.randint(65, 85)
        })
    elif "COPD" in diagnosis:
        vitals.update({
            "spo2": random.randint(88, 92),
            "respiratory_rate": random.randint(18, 24),
            "mode": "SIMV Mode",
            "peep": 6.0,
            "fio2": 30
        })
    
    return vitals

def seed_data():
    # Clear existing data to re-apply correctly
    Patient.objects.all().delete()
    Device.objects.all().delete()
    VitalSign.objects.all().delete()
    Alert.objects.all().delete()

    patients_data = [
        {"full_name": "Rajesh Kumar", "patient_id": "P101", "dob": "1975-05-12", "gender": "Male", "primary_diagnosis": "Severe ARDS", "bed_number": "ICU-01", "physician": "Dr. Sharma", "status": "Critical"},
        {"full_name": "Sneha Sharma", "patient_id": "P102", "dob": "1988-08-22", "gender": "Female", "primary_diagnosis": "Post-Op Recovery", "bed_number": "ICU-02", "physician": "Dr. Verma", "status": "Warning"},
        {"full_name": "Amit Patel", "patient_id": "P103", "dob": "1962-11-30", "gender": "Male", "primary_diagnosis": "Sepsis", "bed_number": "ICU-03", "physician": "Dr. Iyer", "status": "Critical"},
        {"full_name": "Priya Singh", "patient_id": "P104", "dob": "1995-02-15", "gender": "Female", "primary_diagnosis": "Heart Failure", "bed_number": "NICU-01", "physician": "Dr. Reddy", "status": "Warning"},
        {"full_name": "Vikram Singh", "patient_id": "P105", "dob": "1980-03-10", "gender": "Male", "primary_diagnosis": "Pneumonia", "bed_number": "ICU-04", "physician": "Dr. Sharma", "status": "Stable"},
        {"full_name": "Anjali Gupta", "patient_id": "P106", "dob": "1992-07-05", "gender": "Female", "primary_diagnosis": "Asthma Attack", "bed_number": "PICU-01", "physician": "Dr. Gupta", "status": "Stable"},
        {"full_name": "Suresh Raina", "patient_id": "P107", "dob": "1978-12-18", "gender": "Male", "primary_diagnosis": "COPD Exacerbation", "bed_number": "ICU-05", "physician": "Dr. Verma", "status": "Critical"},
        {"full_name": "Meera Iyer", "patient_id": "P108", "dob": "1985-06-25", "gender": "Female", "primary_diagnosis": "Diabetic Ketoacidosis", "bed_number": "ICU-06", "physician": "Dr. Iyer", "status": "Stable"},
        {"full_name": "Rahul Dravid", "patient_id": "P109", "dob": "1970-01-11", "gender": "Male", "primary_diagnosis": "Myocardial Infarction", "bed_number": "CCU-01", "physician": "Dr. Reddy", "status": "Warning"},
        {"full_name": "Kavita Reddy", "patient_id": "P110", "dob": "1990-09-09", "gender": "Female", "primary_diagnosis": "Acute Renal Failure", "bed_number": "ICU-07", "physician": "Dr. Sharma", "status": "Stable"},
        {"full_name": "Manish Malhotra", "patient_id": "P111", "dob": "1965-04-03", "gender": "Male", "primary_diagnosis": "Stroke", "bed_number": "ER-01", "physician": "Dr. Gupta", "status": "Critical"},
        {"full_name": "Pooja Hegde", "patient_id": "P112", "dob": "1983-10-13", "gender": "Female", "primary_diagnosis": "Gastric Perforation", "bed_number": "ICU-08", "physician": "Dr. Verma", "status": "Stable"},
        {"full_name": "Arjun Kapoor", "patient_id": "P113", "dob": "1987-06-26", "gender": "Male", "primary_diagnosis": "Fracture Recovery", "bed_number": "Ward-12", "physician": "Dr. Sharma", "status": "Stable"},
        {"full_name": "Deepa Malik", "patient_id": "P114", "dob": "1972-09-30", "gender": "Female", "primary_diagnosis": "Spinal Injury", "bed_number": "Ward-15", "physician": "Dr. Iyer", "status": "Stable"},
        {"full_name": "Rohit Sharma", "patient_id": "P115", "dob": "1987-04-30", "gender": "Male", "primary_diagnosis": "Post-Op", "bed_number": "ICU-09", "physician": "Dr. Reddy", "status": "Warning"},
        {"full_name": "Vidya Balan", "patient_id": "P116", "dob": "1979-01-01", "gender": "Female", "primary_diagnosis": "Fever", "bed_number": "Ward-05", "physician": "Dr. Sharma", "status": "Stable"},
        {"full_name": "Karan Johar", "patient_id": "P117", "dob": "1972-05-25", "gender": "Male", "primary_diagnosis": "Chest Pain", "bed_number": "ER-05", "physician": "Dr. Verma", "status": "Warning"},
        {"full_name": "Shanti Devi", "patient_id": "P118", "dob": "1955-12-12", "gender": "Female", "primary_diagnosis": "Hypertension", "bed_number": "Ward-10", "physician": "Dr. Gupta", "status": "Stable"},
        {"full_name": "Gopal Das", "patient_id": "P119", "dob": "1968-02-28", "gender": "Male", "primary_diagnosis": "Liver Cirrhosis", "bed_number": "Ward-08", "physician": "Dr. Sharma", "status": "Stable"},
        {"full_name": "Lakshmi Narayan", "patient_id": "P120", "dob": "1982-11-15", "gender": "Female", "primary_diagnosis": "Anemia", "bed_number": "Ward-02", "physician": "Dr. Iyer", "status": "Stable"},
    ]

    for data in patients_data:
        p = Patient.objects.create(
            patient_id=data["patient_id"],
            full_name=data["full_name"],
            dob=data["dob"],
            gender=data["gender"],
            primary_diagnosis=data["primary_diagnosis"],
            bed_number=data["bed_number"],
            attending_physician=data["physician"],
            admission_date=timezone.now().strftime("%Y-%m-%d"),
            status=data["status"]
        )
        
        # Get tailored vitals
        v = get_vitals_by_diagnosis(data["primary_diagnosis"])

        # Create a device and vent settings for each patient
        d = Device.objects.create(
            mac_address=f"MAC:{data['patient_id']}",
            device_type="Ventilator",
            current_settings={
                "mode": v["mode"],
                "peep": str(v["peep"]),
                "fio2": f"{v['fio2']}%",
                "rr": str(v["respiratory_rate"]),
                "tv": str(v["tv"])
            }
        )
        d.assigned_patient = p
        d.save()
        
        VitalSign.objects.create(
            patient=p,
            device=d,
            heart_rate=v["heart_rate"],
            spo2=v["spo2"],
            respiratory_rate=v["respiratory_rate"],
            blood_pressure_sys=v["bp_sys"],
            blood_pressure_dia=v["bp_dia"],
            temperature=v["temp"],
            fio2=float(v["fio2"]),
            vte=float(v["tv"])
        )

    # Add 4 alerts to the critical/warning patients
    p1 = Patient.objects.get(patient_id="P101")
    Alert.objects.create(patient=p1, alert_type="Critical", description="High Heart Rate (Tachycardia)", current_value="115 bpm", limit_value="100 bpm", ai_confidence=85, status="Active")

    p2 = Patient.objects.get(patient_id="P102")
    Alert.objects.create(patient=p2, alert_type="Warning", description="Low SpO2 level detected", current_value="91%", limit_value="94%", ai_confidence=92, status="Active")

    p3 = Patient.objects.get(patient_id="P103")
    Alert.objects.create(patient=p3, alert_type="Critical", description="Sudden drop in Blood Pressure", current_value="90/60", limit_value="110/70", ai_confidence=88, status="Active")

    p4 = Patient.objects.get(patient_id="P104")
    Alert.objects.create(patient=p4, alert_type="Warning", description="Irregular Respiratory Rate", current_value="28 bpm", limit_value="20 bpm", ai_confidence=75, status="Active")

    print("Success: 20 Indian Patients (Tailored Vitals) and 4 Alerts seeded.")

if __name__ == "__main__":
    seed_data()
