import uuid

def test_tick_analysis(client):
    m_id = f"m_tick_{uuid.uuid4().hex[:8]}"
    t_id = f"trig_tick_{uuid.uuid4().hex[:8]}"

    # Setup merchant context
    client.post("/v1/context", json={
        "scope": "merchant",
        "context_id": m_id,
        "version": 1,
        "data": {
            "merchant_id": m_id,
            "name": "Smile Dent",
            "vertical": "dentists",
            "locality": "Indiranagar",
            "offers": [{"title": "Dental Check Up", "discounted_price": 299, "active": True}],
            "metrics": {"searches_in_locality": 190}
        }
    })

    # Setup trigger context
    client.post("/v1/context", json={
        "scope": "trigger",
        "context_id": t_id,
        "version": 1,
        "data": {
            "trigger_id": t_id,
            "type": "SEARCH_SPIKE",
            "value": 190,
            "metric": "searches"
        }
    })

    # Post Tick
    r = client.post("/v1/tick", json={
        "merchant_id": m_id,
        "trigger_id": t_id,
        "dry_run": True
    })
    assert r.status_code == 200
    res = r.json()
    assert res["status"] == "acted"
    assert "190" in res["message"] or "Dental Check Up" in res["message"]
    assert res["cta"] is not None
    assert "299" in res["cta"] or "299" in res["message"]
