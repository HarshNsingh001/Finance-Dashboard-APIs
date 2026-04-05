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
            name="Admin User",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role=Role.ADMIN,
            is_active=True,
        )
        analyst = User(
            name="Analyst User",
            email="analyst@example.com",
            hashed_password=hash_password("analyst123"),
            role=Role.ANALYST,
            is_active=True,
        )
        viewer = User(
            name="Viewer User",
            email="viewer@example.com",
            hashed_password=hash_password("viewer123"),
            role=Role.VIEWER,
            is_active=True,
        )

        db.add_all([admin, analyst, viewer])
        db.flush()

        print(" Creating financial records...")

        records = [
            FinancialRecord(
                amount=5000.00,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 1, 15),
                description="January salary",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5000.00,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 2, 15),
                description="February salary",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5200.00,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 3, 15),
                description="March salary with bonus",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5000.00,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 4, 15),
                description="April salary",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=5000.00,
                type=RecordType.INCOME,
                category="Salary",
                date=date(2024, 5, 15),
                description="May salary",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1200.00,
                type=RecordType.INCOME,
                category="Freelance",
                date=date(2024, 2, 20),
                description="Web development project",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=800.00,
                type=RecordType.INCOME,
                category="Freelance",
                date=date(2024, 4, 10),
                description="Logo design project",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=500.00,
                type=RecordType.INCOME,
                category="Investment",
                date=date(2024, 3, 1),
                description="Dividend payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=350.00,
                type=RecordType.INCOME,
                category="Investment",
                date=date(2024, 5, 1),
                description="Interest on savings",
                created_by_id=admin.id,
            ),
            # Expense records
            FinancialRecord(
                amount=1500.00,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 1, 1),
                description="Monthly rent payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.00,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 2, 1),
                description="Monthly rent payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.00,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 3, 1),
                description="Monthly rent payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.00,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 4, 1),
                description="Monthly rent payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=1500.00,
                type=RecordType.EXPENSE,
                category="Rent",
                date=date(2024, 5, 1),
                description="Monthly rent payment",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=450.00,
                type=RecordType.EXPENSE,
                category="Groceries",
                date=date(2024, 1, 10),
                description="Monthly groceries",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=380.00,
                type=RecordType.EXPENSE,
                category="Groceries",
                date=date(2024, 2, 8),
                description="Monthly groceries",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=120.00,
                type=RecordType.EXPENSE,
                category="Utilities",
                date=date(2024, 1, 20),
                description="Electricity bill",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=85.00,
                type=RecordType.EXPENSE,
                category="Utilities",
                date=date(2024, 2, 20),
                description="Internet bill",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=200.00,
                type=RecordType.EXPENSE,
                category="Transportation",
                date=date(2024, 3, 15),
                description="Monthly transit pass",
                created_by_id=admin.id,
            ),
            FinancialRecord(
                amount=75.00,
                type=RecordType.EXPENSE,
                category="Entertainment",
                date=date(2024, 4, 20),
                description="Streaming subscriptions",
                created_by_id=admin.id,
            ),
        ]

        db.add_all(records)
        db.commit()

        print()
        print("✅ Database seeded successfully!")
        print()
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                    Default User Accounts                    ║")
        print("╠══════════════════════════╦═══════════════╦══════════════════╣")
        print("║ Email                    ║ Password      ║ Role             ║")
        print("╠══════════════════════════╬═══════════════╬══════════════════╣")
        print("║ admin@example.com        ║ admin123      ║ ADMIN            ║")
        print("║ analyst@example.com      ║ analyst123    ║ ANALYST          ║")
        print("║ viewer@example.com       ║ viewer123     ║ VIEWER           ║")
        print("╚══════════════════════════╩═══════════════╩══════════════════╝")
        print()
        print(f" Created {len(records)} financial records.")

    except Exception as e:
        db.rollback()
        print(f" Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
