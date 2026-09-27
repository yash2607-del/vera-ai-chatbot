def test_missing_merchant_fallback(client):
    # Tick for unknown merchant should not crash, but return valid fallback recommendation
    r = client.post("/v1/tick", json={"merchant_id": "non_existent_merchant_xyz", "dry_run": True})
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "acted"
    assert res["message"] is not None

def test_malformed_context_scope(client):
    r = client.post("/v1/context", json={
        "scope": "invalid_scope_abc",
        "context_id": "c1",
        "version": 1,
        "data": {}
    })
    assert r.status_code == 400
