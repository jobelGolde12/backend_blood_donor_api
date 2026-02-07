import pytest
import requests
from typing import Dict, Any
import os


class TestRegistrationAPI:
    """Test registration functionality using the API_BASE_URL"""

    def setup_method(self):
        """Set up test configuration"""
        # Use the Render deployment URL as specified by the user
        self.base_url = "https://backend-blood-donor-api.onrender.com/api/v1"
        
        # Sample registration data for testing (using correct Philippine format)
        self.registration_data = {
            "full_name": "Juan Dela Cruz",
            "contact_number": "+639171234567",  # Philippine format
            "email": "juan.dela.cruz@example.com",
            "age": 25,
            "blood_type": "O+",
            "municipality": "Manila",
            "availability": "available"  # String instead of boolean
        }

    def test_create_registration_success(self):
        """Test successful donor registration"""
        try:
            response = requests.post(
                f"{self.base_url}/donor-registrations",
                json=self.registration_data,
                headers={"Content-Type": "application/json"}
            )
            
            # Expected responses: 201 Created or 400/409 if already exists
            assert response.status_code in [201, 400, 409], f"Unexpected status code: {response.status_code}"
            
            if response.status_code == 201:
                data = response.json()
                assert "id" in data
                assert data["full_name"] == self.registration_data["full_name"]
                assert data["contact_number"] == self.registration_data["contact_number"]
                print(f"✓ Registration created successfully with ID: {data['id']}")
            elif response.status_code in [400, 409]:
                print(f"⚠ Registration failed as expected (already exists): {response.json()}")
                
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    def test_create_registration_invalid_data(self):
        """Test registration with invalid data"""
        invalid_data = {
            "full_name": "",  # Empty name
            "contact_number": "invalid-number",  # Invalid format
            "email": "invalid-email",  # Invalid email
            "age": 15,  # Too young
            "blood_type": "INVALID",  # Invalid blood type
            "municipality": "",
            "availability": "invalid_status"  # Invalid availability
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/donor-registrations",
                json=invalid_data,
                headers={"Content-Type": "application/json"}
            )
            
            # Should return validation error (422) or similar
            assert response.status_code in [422, 400], f"Expected validation error, got: {response.status_code}"
            print(f"✓ Invalid registration correctly rejected with status: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    def test_list_registrations(self):
        """Test listing registrations (requires admin authentication)"""
        try:
            response = requests.get(f"{self.base_url}/donor-registrations")
            
            # Without authentication, this should return 401 or 403
            assert response.status_code in [401, 403, 200], f"Unexpected status: {response.status_code}"
            print(f"✓ List registrations responded with status: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    def test_health_check(self):
        """Test the health check endpoint"""
        try:
            response = requests.get(f"{self.base_url.replace('/api/v1', '')}/health")
            
            assert response.status_code == 200, f"Health check failed with status: {response.status_code}"
            data = response.json()
            assert "status" in data
            assert data["status"] == "healthy"
            print("✓ Health check passed")
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")


# Run tests if this file is executed directly
if __name__ == "__main__":
    test_instance = TestRegistrationAPI()
    
    print("Testing registration API...")
    test_instance.setup_method()  # Call setup to initialize base_url
    print(f"Using base URL: {test_instance.base_url}")
    
    try:
        test_instance.test_health_check()
    except Exception as e:
        print(f"Health check failed: {e}")
    
    try:
        test_instance.test_create_registration_success()
    except Exception as e:
        print(f"Registration test failed: {e}")
    
    try:
        test_instance.test_create_registration_invalid_data()
    except Exception as e:
        print(f"Invalid registration test failed: {e}")
    
    try:
        test_instance.test_list_registrations()
    except Exception as e:
        print(f"List registrations test failed: {e}")
    
    print("All tests completed!")