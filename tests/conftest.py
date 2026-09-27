import os
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    os.environ["DATABASE_PATH"] = "sqlite:///./test_vera.db"
    init_db()
    yield
    if os.path.exists("test_vera.db"):
        try:
            os.remove("test_vera.db")
        except PermissionError:
            pass

@pytest.fixture
def client():
    return TestClient(app)
