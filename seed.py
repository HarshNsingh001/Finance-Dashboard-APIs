import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import engine, Base, SessionLocal
from app.models.user import User, Role
from app.models.record import FinancialRecord, RecordType
from app.utils.security import hash_password


def seed_database():
    print(" Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        existing_users = db.query(User).count()
        if existing_users > 0:
            print("  Database already has data. Skipping seed.")
            print(f"   Found {existing_users} users.")
            return

        print(" Creating users...")

        admin = User(
            name="Harsh Singh",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role=Role.ADMIN,
        )
        analyst = User(
            name="Analyst Team",
            email="analyst@example.com",
            hashed_password=hash_password("analyst123"),
            role=Role.ANALYST,
        )
        viewer = User(
            name="Viewer Account",
            email="viewer@example.com",
            hashed_password=hash_password("viewer123"),
            role=Role.VIEWER,
        )

        db.add_all([admin, analyst, viewer])
        db.flush()

        print(" Creating financial records...")

        records = [
            FinancialRecord(
                amount=5000.0,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 1, 15),
                description="Salary - Jan",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5000.0,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 2, 15),
                description="Monthly payout (Feb)",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5250.0,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 3, 15),
                description="Base salary + Bonus",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5000.0,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 4, 15),
                description="Apr Monthly Salary",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5000.0,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 5, 15),
                description="Salary - May",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1200.0,
                type=RecordType.INCOME,
                category="Freelance",
                date=date(2024, 2, 20),
                description="Web dev project P1",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=850.0,
                type=RecordType.INCOME,
                category="Freelance",
                date=date(2024, 4, 10),
                description="Logo design - Client G",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=500.0,
                type=RecordType.INCOME,
                category="Investment",
                date=date(2024, 3, 1),
                description="Stock dividend",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=350.0,
                type=RecordType.INCOME,
                category="Investment",
                date=date(2024, 5, 1),
                description="Savings interest",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.0,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 1, 1),
                description="Apartment Rent - Jan",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.0,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 2, 1),
                description="Feb Rent payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.00,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 3, 1),
                description="Rent - March",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.0,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 4, 1),
                description="Apr Monthly Rent",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.0,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 5, 1),
                description="Rent payment (May)",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=450.0,
                type=RecordType.EXPENSE,
                category="Groceries",
                date=date(2024, 1, 10),
                description="Store run - Jan",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=385.0,
                type=RecordType.EXPENSE,
                category="Groceries",
                date=date(2024, 2, 8),
                description="Weekly Groceries",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=120.0,
                type=RecordType.EXPENSE,
                category="Utilities",
                date=date(2024, 1, 20),
                description="Electricity Bill",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=85.0,
                type=RecordType.EXPENSE,
                category="Utilities",
                date=date(2024, 2, 20),
                description="Airtel Broadband",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=200.0,
                type=RecordType.EXPENSE,
                category="Transportation",
                date=date(2024, 3, 15),
                description="Fuel & Tolls",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=75.0,
                type=RecordType.EXPENSE,
                category="Entertainment",
                date=date(2024, 4, 20),
                description="Netflix / Hotstar",
                created_by_id=admin.id,
            ),
        ]

        db.add_all(records)
        db.commit()

        print("\nSeed completed successfully!")
        print("-" * 30)
        print("Test Accounts Created:")
        print("Admin:   admin@example.com / admin123")
        print("Analyst: analyst@example.com / analyst123")
        print("Viewer:  viewer@example.com / viewer123")
        print("-" * 30)
        print(f"Added {len(records)} records to the database.")

    except Exception as e:
        db.rollback()
        print(f" Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
