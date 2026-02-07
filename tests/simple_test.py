import requests

def test_api_with_correct_data():
    """Test the API with correct data format"""
    base_url = "https://backend-blood-donor-api.onrender.com/api/v1"
    
    # Correct data format for the deployed API
    registration_data = {
        "full_name": "Maria Santos",
        "contact_number": "+639171234567",  # Philippine format
        "email": "maria.santos@example.com",
        "age": 28,
        "blood_type": "O+",
        "municipality": "Quezon City",
        "availability": "available"  # String instead of boolean
    }

    print("Testing registration API with correct format...")
    print(f"Using base URL: {base_url}")
    
    try:
        response = requests.post(
            f"{base_url}/donor-registrations",
            json=registration_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}...")  # Truncate long responses
        
        if response.status_code in [201, 400, 409]:
            print("✓ API is working correctly with proper validation")
        else:
            print(f"⚠ Unexpected status: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print("⚠ Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except Exception as e:
        print(f"Test failed with error: {e}")


if __name__ == "__main__":
    test_api_with_correct_data()