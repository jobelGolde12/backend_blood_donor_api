import requests
from typing import Dict, Any


def test_registration_with_details():
    """Test registration functionality and get detailed error information"""
    # Use the Render deployment URL as specified by the user
    base_url = "https://backend-blood-donor-api.onrender.com/api/v1"
    
    # Sample registration data for testing (using correct Philippine format)
    registration_data = {
        "full_name": "Juan Dela Cruz",
        "contact_number": "+639171234567",  # Philippine format
        "email": "juan.dela.cruz@example.com",
        "age": 25,
        "blood_type": "O+",
        "municipality": "Manila",
        "availability": "available"  # String instead of boolean
    }

    print("Testing registration API...")
    print(f"Using base URL: {base_url}")
    
    # Test health check first
    try:
        health_response = requests.get(f"{base_url.replace('/api/v1', '')}/health")
        print(f"✓ Health check responded with status: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"  Health data: {health_response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

    # Test registration endpoint
    try:
        response = requests.post(
            f"{base_url}/donor-registrations",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Registration request responded with status: {response.status_code}")
        print(f"Response body: {response.text}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 500:
            print("❌ Server Error - this indicates an issue with the deployed API")
            print("Possible causes:")
            print("  - Database connection issue")
            print("  - Missing environment variables")
            print("  - Internal server error")
        elif response.status_code == 201:
            print("✓ Registration created successfully")
        elif response.status_code in [400, 409]:
            print("⚠ Registration failed as expected (likely already exists)")
        else:
            print(f"⚠ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
    except Exception as e:
        print(f"Test failed with error: {str(e)}")


if __name__ == "__main__":
    test_registration_with_details()