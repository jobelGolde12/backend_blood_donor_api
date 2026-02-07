"""
Seed realistic Philippine-based data for Blood Donor API
Run after migrations: python seed_data.py
"""
import asyncio
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.user import User, UserRole, UserStatus
from app.models.donor import DonorRegistration, DonorProfile, BloodType, AvailabilityStatus, RegistrationStatus
from app.models.message import Message
from app.models.notification import Alert, Notification, AlertType, Priority, NotificationType

engine = create_engine(str(settings.database_url))
SessionLocal = sessionmaker(bind=engine)

# Philippine-specific data
FILIPINO_NAMES = [
    "Juan Dela Cruz", "Maria Clara Santos", "Jose Rizal Reyes", "Ana Marie Garcia",
    "Mark Anthony Bautista", "Princess Joy Mendoza", "John Paul Villanueva",
    "Mary Grace Fernandez", "Angelo Miguel Torres", "Kristine Mae Ramos",
    "Joshua Emmanuel Cruz", "Angel Faith Gonzales", "Christian James Lopez",
    "Angelica Rose Aquino", "Francis Xavier Castillo", "Jasmine Nicole Flores",
    "Rafael Antonio Morales", "Catherine Anne Santiago", "Miguel Angelo Pascual",
    "Stephanie Marie Diaz"
]

PH_MUNICIPALITIES = [
    "Quezon City", "Manila", "Cebu City", "Davao City", "Caloocan", 
    "Makati", "Pasig", "Taguig", "Parañaque", "Las Piñas",
    "Antipolo", "Cagayan de Oro", "Zamboanga City", "Iloilo City",
    "San Fernando, Pampanga", "Bacoor, Cavite", "General Santos", "Bacolod"
]

BLOOD_TYPES = [
    (BloodType.O_POSITIVE, 0.35),
    (BloodType.A_POSITIVE, 0.28),
    (BloodType.B_POSITIVE, 0.20),
    (BloodType.AB_POSITIVE, 0.08),
    (BloodType.O_NEGATIVE, 0.04),
    (BloodType.A_NEGATIVE, 0.03),
    (BloodType.B_NEGATIVE, 0.015),
    (BloodType.AB_NEGATIVE, 0.005)
]

def weighted_blood_type():
    import random
    return random.choices([bt for bt, _ in BLOOD_TYPES], weights=[w for _, w in BLOOD_TYPES])[0]

def generate_ph_mobile():
    import random
    prefixes = ['0915', '0916', '0917', '0926', '0927', '0935', '0936', '0945', '0955', '0956', '0965', '0975', '0995', '0905', '0906']
    return f"{random.choice(prefixes)}{random.randint(1000000, 9999999)}"

def seed_database():
    db = SessionLocal()
    try:
        # Check if already seeded
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"⚠️  Database already has {existing_users} users. Skipping seed.")
            return
        
        print("🌱 Seeding database with Philippine data...")
        
        # 1. Create admin user
        admin = User(
            full_name="Admin User",
            contact_number="09171234567",
            email="admin@blooddonor.ph",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            created_at=datetime.utcnow()
        )
        db.add(admin)
        db.flush()
        print(f"✅ Created admin user (ID: {admin.id})")
        
        # 2. Create donor registrations and profiles
        import random
        donor_users = []
        donor_profiles = []
        
        for i, name in enumerate(FILIPINO_NAMES):
            # Create registration
            status = random.choices(
                [RegistrationStatus.APPROVED, RegistrationStatus.PENDING, RegistrationStatus.REJECTED],
                weights=[0.7, 0.2, 0.1]
            )[0]
            
            blood_type = weighted_blood_type()
            contact = generate_ph_mobile()
            municipality = random.choice(PH_MUNICIPALITIES)
            age = random.randint(18, 60)
            
            registration = DonorRegistration(
                full_name=name,
                contact_number=contact,
                email=f"{name.lower().replace(' ', '.')}@email.com" if random.random() > 0.3 else None,
                age=age,
                blood_type=blood_type,
                municipality=municipality,
                availability=AvailabilityStatus.AVAILABLE,
                status=status,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90))
            )
            
            if status in [RegistrationStatus.APPROVED, RegistrationStatus.REJECTED]:
                registration.reviewed_by = admin.id
                registration.reviewed_at = registration.created_at + timedelta(hours=random.randint(1, 48))
                if status == RegistrationStatus.REJECTED:
                    registration.review_reason = random.choice([
                        "Incomplete medical history",
                        "Does not meet age requirement",
                        "Recent medical condition reported"
                    ])
            
            db.add(registration)
            db.flush()
            
            # Create user and profile for approved registrations
            if status == RegistrationStatus.APPROVED:
                user = User(
                    full_name=name,
                    contact_number=contact,
                    email=registration.email,
                    role=UserRole.DONOR,
                    status=UserStatus.ACTIVE,
                    created_at=registration.reviewed_at
                )
                db.add(user)
                db.flush()
                donor_users.append(user)
                
                availability = random.choices(
                    [AvailabilityStatus.AVAILABLE, AvailabilityStatus.UNAVAILABLE, AvailabilityStatus.RECENTLY_DONATED],
                    weights=[0.6, 0.2, 0.2]
                )[0]
                
                profile = DonorProfile(
                    user_id=user.id,
                    registration_id=registration.id,
                    age=age,
                    blood_type=blood_type,
                    municipality=municipality,
                    availability=availability,
                    created_at=user.created_at
                )
                db.add(profile)
                db.flush()
                donor_profiles.append(profile)
        
        print(f"✅ Created {len(FILIPINO_NAMES)} registrations")
        print(f"✅ Created {len(donor_users)} donor users and profiles")
        
        # 3. Create messages
        message_subjects = [
            "Question about donation eligibility",
            "Update my contact information",
            "When is the next blood drive?",
            "I want to donate but have concerns",
            "Availability update needed"
        ]
        
        for i in range(min(8, len(donor_profiles))):
            profile = random.choice(donor_profiles)
            message = Message(
                donor_profile_id=profile.id,
                subject=random.choice(message_subjects),
                content=f"Hello admin, I would like to inquire about {random.choice(['donation schedule', 'eligibility requirements', 'blood drive locations', 'my donor status'])}. Thank you!",
                is_closed=random.choice([True, False]),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(message)
        
        print(f"✅ Created messages")
        
        # 4. Create alerts
        alerts_data = [
            {
                "title": "Urgent O+ Blood Needed – Philippine General Hospital",
                "message": "We urgently need O+ blood donors for emergency surgery patients at PGH. Please respond if available.",
                "alert_type": AlertType.URGENT_REQUEST,
                "priority": Priority.CRITICAL,
                "target_audience": {"blood_types": ["O+"], "municipalities": ["Manila", "Quezon City", "Makati"]}
            },
            {
                "title": "Red Cross Mobile Blood Drive – Quezon City",
                "message": "Join us this Saturday at SM North EDSA for our quarterly blood donation drive. Free snacks and health screening!",
                "alert_type": AlertType.DONATION_DRIVE,
                "priority": Priority.MEDIUM,
                "target_audience": {"municipalities": ["Quezon City", "Caloocan", "Valenzuela"]}
            },
            {
                "title": "AB- Blood Urgently Required – St. Luke's Medical Center",
                "message": "Critical need for AB- blood type. Patient requires immediate transfusion. Contact us ASAP.",
                "alert_type": AlertType.URGENT_REQUEST,
                "priority": Priority.CRITICAL,
                "target_audience": {"blood_types": ["AB-", "AB+"]}
            },
            {
                "title": "Thank You to All Our Donors!",
                "message": "We've reached 1,000 successful donations this year. Thank you for saving lives!",
                "alert_type": AlertType.GENERAL_ANNOUNCEMENT,
                "priority": Priority.LOW,
                "target_audience": None
            },
            {
                "title": "Blood Donation Camp – Cebu City",
                "message": "Free blood donation camp at Ayala Center Cebu this weekend. Walk-ins welcome!",
                "alert_type": AlertType.DONATION_DRIVE,
                "priority": Priority.MEDIUM,
                "target_audience": {"municipalities": ["Cebu City", "Mandaue", "Lapu-Lapu"]}
            }
        ]
        
        created_alerts = []
        for alert_data in alerts_data:
            send_now = random.choice([True, False])
            alert = Alert(
                title=alert_data["title"],
                message=alert_data["message"],
                alert_type=alert_data["alert_type"],
                priority=alert_data["priority"],
                target_audience=alert_data["target_audience"],
                send_now=send_now,
                schedule_at=None if send_now else datetime.utcnow() + timedelta(days=random.randint(1, 7)),
                sent_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72)) if send_now else None,
                created_by=admin.id,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(alert)
            db.flush()
            created_alerts.append(alert)
        
        print(f"✅ Created {len(alerts_data)} alerts")
        
        # 5. Create notifications from sent alerts
        notification_count = 0
        for alert in created_alerts:
            if alert.sent_at:
                # Send to matching donors
                for user in donor_users[:random.randint(5, len(donor_users))]:
                    notification = Notification(
                        user_id=user.id,
                        title=alert.title,
                        message=alert.message,
                        notification_type=NotificationType.ALERT,
                        is_read=random.choice([True, False]),
                        alert_id=alert.id,
                        created_at=alert.sent_at
                    )
                    db.add(notification)
                    notification_count += 1
        
        # Add some system notifications
        for user in donor_users[:5]:
            notification = Notification(
                user_id=user.id,
                title="Welcome to Blood Donor Network!",
                message="Thank you for registering as a blood donor. Your profile has been approved.",
                notification_type=NotificationType.SYSTEM,
                is_read=random.choice([True, False]),
                created_at=user.created_at
            )
            db.add(notification)
            notification_count += 1
        
        print(f"✅ Created {notification_count} notifications")
        
        db.commit()
        print("\n🎉 Database seeded successfully!")
        print(f"\n📊 Summary:")
        print(f"   - 1 admin user")
        print(f"   - {len(FILIPINO_NAMES)} donor registrations")
        print(f"   - {len(donor_users)} approved donors")
        print(f"   - {len(alerts_data)} alerts")
        print(f"   - {notification_count} notifications")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Starting database seed...")
    seed_database()
