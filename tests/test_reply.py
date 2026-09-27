def test_reply_state_machine(client):
    conv_id = "conv_test_reply_1"
    m_id = "m_reply_01"

    # 1. Test Accept
    r1 = client.post("/v1/reply", json={
        "merchant_id": m_id,
        "conversation_id": conv_id,
        "merchant_message": "yes go ahead"
    })
    assert r1.status_code == 200
    assert r1.json()["current_state"] == "ACTION_CONFIRMED"

    # 2. Test Off-Topic
    r2 = client.post("/v1/reply", json={
        "merchant_id": m_id,
        "conversation_id": conv_id,
        "merchant_message": "tell me a joke"
    })
    assert r2.status_code == 200
    assert r2.json()["current_state"] == "OFF_TOPIC"
