def test_metadata_endpoint(client):
    response = client.get("/v1/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "supported_verticals" in data
    assert len(data["supported_verticals"]) == 5
    assert "dentists" in data["supported_verticals"]
