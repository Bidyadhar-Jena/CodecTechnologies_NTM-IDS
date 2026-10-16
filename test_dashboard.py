from app import app

def test_dashboard():
    client = app.test_client()

    # Test the home page
    response = client.get("/")
    print("Home page:", response.status_code)
    assert response.status_code == 200

    # Test live traffic endpoint
    response = client.get("/api/traffic")
    print("Traffic API:", response.status_code)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

    # Test live alerts endpoint
    response = client.get("/api/alerts")
    print("Live alerts API:", response.status_code)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

    # Test database alert history
    response = client.get("/api/alerts/history")
    print("Alert history API:", response.status_code)
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

    # Test dashboard statistics
    response = client.get("/api/stats")
    print("Statistics API:", response.status_code)
    assert response.status_code == 200

    print("\nAll dashboard API tests passed!")


if __name__ == "__main__":
    test_dashboard()