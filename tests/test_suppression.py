import uuid

def test_suppression_guardrail(client):
    m_id = f"m_supp_test_{uuid.uuid4().hex[:8]}"
    
    # First tick -> acted
    r1 = client.post("/v1/tick", json={"merchant_id": m_id, "dry_run": False})
    assert r1.status_code == 200
    assert r1.json()["status"] == "acted"

    # Second tick with same parameters -> suppressed
    r2 = client.post("/v1/tick", json={"merchant_id": m_id, "dry_run": False})
    assert r2.status_code == 200
    assert r2.json()["status"] == "suppressed"
