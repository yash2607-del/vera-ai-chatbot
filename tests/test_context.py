def test_context_ingestion_and_versioning(client):
    # 1. Post version 1
    p1 = {
        "scope": "merchant",
        "context_id": "m_test_101",
        "version": 1,
        "data": {"name": "Test Clinic", "vertical": "dentists"}
    }
    r1 = client.post("/v1/context", json=p1)
    assert r1.status_code == 200
    assert r1.json()["status"] == "success"

    # 2. Post version 2 (newer)
    p2 = {
        "scope": "merchant",
        "context_id": "m_test_101",
        "version": 2,
        "data": {"name": "Test Clinic Updated", "vertical": "dentists"}
    }
    r2 = client.post("/v1/context", json=p2)
    assert r2.status_code == 200
    assert r2.json()["version"] == 2

    # 3. Post version 1 again (older version should be skipped/rejected)
    p3 = {
        "scope": "merchant",
        "context_id": "m_test_101",
        "version": 1,
        "data": {"name": "Old Clinic", "vertical": "dentists"}
    }
    r3 = client.post("/v1/context", json=p3)
    assert r3.status_code == 200
