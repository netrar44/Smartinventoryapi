import json
import app as inventory_app
 
 
def prepare_database(monkeypatch, tmp_path):
    test_file = tmp_path / "inventory.json"
    test_file.write_text("[]", encoding="utf-8")
 
    monkeypatch.setattr(
        inventory_app, "DB_FILE", test_file
    )
 
    return inventory_app.app.test_client()
 
 
def test_home():
    client = inventory_app.app.test_client()
 
    response = client.get("/")
 
    assert response.status_code == 200
    assert "Smart Inventory API" in response.get_json()["message"]
 
 
def test_get_inventory(monkeypatch, tmp_path):
    client = prepare_database(monkeypatch, tmp_path)
 
    response = client.get("/inventory")
 
    assert response.status_code == 200
    assert response.get_json() == []
 
 
def test_add_item(monkeypatch, tmp_path):
    client = prepare_database(monkeypatch, tmp_path)
 
    item = {
        "ProductID": "TEST001",
        "ProductName": "Wire Coil",
        "Stock": 20,
        "Price": 300.0
    }
 
    response = client.post("/add", json=item)
 
    assert response.status_code == 201
    assert response.get_json()["success"] is True
 
    # Verify the data was saved
    saved_data = json.loads(
        (tmp_path / "inventory.json").read_text(encoding="utf-8")
    )
 
    assert len(saved_data) == 1
    assert saved_data[0]["ProductID"] == "TEST001"
 
 
def test_duplicate_product(monkeypatch, tmp_path):
    client = prepare_database(monkeypatch, tmp_path)
 
    item = {
        "ProductID": "TEST001",
        "ProductName": "Wire Coil",
        "Stock": 20,
        "Price": 300.0
    }
 
    first_response = client.post("/add", json=item)
    second_response = client.post("/add", json=item)
 
    assert first_response.status_code == 201
    assert second_response.status_code == 409