import pytest
from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.dependencies import get_db
from app.main import app
from app.models.user import User, Role
from app.models.record import FinancialRecord, RecordType
from app.utils.security import hash_password, create_access_token


TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_user(db) -> User:
    user = User(
        name="Test Admin",
        email="admin@test.com",
        hashed_password=hash_password("admin123"),
        role=Role.ADMIN,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def analyst_user(db) -> User:
    user = User(
        name="Test Analyst",
        email="analyst@test.com",
        hashed_password=hash_password("analyst123"),
        role=Role.ANALYST,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def viewer_user(db) -> User:
    user = User(
        name="Test Viewer",
        email="viewer@test.com",
        hashed_password=hash_password("viewer123"),
        role=Role.VIEWER,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_headers(admin_user) -> dict:
    token = create_access_token({"sub": admin_user.id, "role": admin_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def analyst_headers(analyst_user) -> dict:
    token = create_access_token(
        {"sub": analyst_user.id, "role": analyst_user.role.value}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def viewer_headers(viewer_user) -> dict:
    token = create_access_token({"sub": viewer_user.id, "role": viewer_user.role.value})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_records(db, admin_user) -> list[FinancialRecord]:
    records = [
        FinancialRecord(
            amount=5000.00,
            type=RecordType.INCOME,
            category="Salary",
            date=date(2024, 1, 15),
            description="January salary",
            created_by_id=admin_user.id,
        ),
        FinancialRecord(
            amount=1200.00,
            type=RecordType.INCOME,
            category="Freelance",
            date=date(2024, 2, 20),
            description="Web project",
            created_by_id=admin_user.id,
        ),
        FinancialRecord(
            amount=1500.00,
            type=RecordType.EXPENSE,
            category="Rent",
            date=date(2024, 1, 1),
            description="Monthly rent",
            created_by_id=admin_user.id,
        ),
        FinancialRecord(
            amount=450.00,
            type=RecordType.EXPENSE,
            category="Groceries",
            date=date(2024, 1, 10),
            description="Monthly groceries",
            created_by_id=admin_user.id,
        ),
        FinancialRecord(
            amount=120.00,
            type=RecordType.EXPENSE,
            category="Utilities",
            date=date(2024, 2, 20),
            description="Electricity bill",
            created_by_id=admin_user.id,
        ),
    ]
    db.add_all(records)
    db.commit()
    for r in records:
        db.refresh(r)
    return records
