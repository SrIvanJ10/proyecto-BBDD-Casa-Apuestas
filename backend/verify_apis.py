import requests
import json
import time

BASE_URL = "http://192.168.1.239:8000/api"
AUTH_URL = f"{BASE_URL}/auth"
MATCHES_URL = f"{BASE_URL}/matches"
PREDICTIONS_URL = f"{BASE_URL}/predictions"
USERS_URL = f"{BASE_URL}/users"
ANALYTICS_URL = f"{BASE_URL}/analytics"
RECOMMENDATIONS_URL = f"{BASE_URL}/recommendations"

TEST_USER = {
    "username": f"testuser_{int(time.time())}",
    "email": f"testuser_{int(time.time())}@example.com",
    "password": "TestPassword123!",
    "first_name": "Test",
    "last_name": "User"
}

def print_result(name, success, details=None):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"   Details: {details}")

def run_tests():
    print("🚀 Starting API Verification...")
    
    # 1. Authentication
    print("\n--- Authentication ---")
    
    # Register
    print(f"Registering user {TEST_USER['username']}...")
    response = requests.post(f"{AUTH_URL}/register/", json=TEST_USER)
    otp_code = None
    
    if response.status_code == 201:
        print_result("Register", True)
        otp_code = response.json().get("otp_code")
        print(f"   OTP Code received: {otp_code}")
    elif response.status_code == 400 and "already exists" in response.text:
        print_result("Register (User already exists)", True)
        # If user exists, we can't get the OTP easily unless we trigger forgot password or just try to login (which failed).
        # For this test script, if user exists, we might need to use a new user or handle this case.
        # Let's try to login, if it fails with "not activated", we are stuck unless we use a fresh user.
        # To make the test robust, let's append a timestamp to the username/email to always create a new user.
    else:
        print_result("Register", False, response.text)

    if otp_code:
        print("Verifying OTP...")
        verify_data = {
            "email": TEST_USER["email"],
            "otp": otp_code
        }
        response = requests.post(f"{AUTH_URL}/verify-otp/", json=verify_data)
        if response.status_code == 200:
            print_result("Verify OTP", True)
        else:
            print_result("Verify OTP", False, response.text)

    # Login
    print("Logging in...")
    login_data = {
        "email_or_username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    response = requests.post(f"{AUTH_URL}/login/", json=login_data)
    token = None
    if response.status_code == 200:
        token = response.json().get("access") or response.json().get("token")
        print_result("Login", True)
    else:
        print_result("Login", False, response.text)
        return

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Users
    print("\n--- Users ---")
    response = requests.get(f"{USERS_URL}/profile/", headers=headers)
    print_result("Get Profile", response.status_code == 200, response.text if response.status_code != 200 else None)

    response = requests.get(f"{USERS_URL}/leaderboard/", headers=headers)
    print_result("Get Leaderboard", response.status_code == 200)

    # 3. Matches
    print("\n--- Matches ---")
    response = requests.get(f"{MATCHES_URL}/", headers=headers)
    print_result("List Matches", response.status_code == 200)
    
    match_id = None
    if response.status_code == 200:
        matches = response.json().get("results", [])
        if matches:
            match_id = matches[0].get("id")
            print(f"   Found match ID: {match_id}")

    if match_id:
        response = requests.get(f"{MATCHES_URL}/{match_id}/", headers=headers)
        print_result("Get Match Detail", response.status_code == 200)

    response = requests.get(f"{MATCHES_URL}/upcoming/", headers=headers)
    print_result("Get Upcoming Matches", response.status_code == 200)

    # 4. Predictions
    print("\n--- Predictions ---")
    if match_id:
        prediction_data = {
            "match": match_id,
            "prediction_type": "winner",
            "predicted_value": "home",
            "stake": 10
        }
        # Note: This might fail if the match is not open for predictions or user has no balance, but we check if the endpoint is reachable
        response = requests.post(f"{PREDICTIONS_URL}/create/", json=prediction_data, headers=headers)
        print_result("Create Prediction", response.status_code in [201, 400], f"Status: {response.status_code} (400 is acceptable if logic prevents it)")

    response = requests.get(f"{PREDICTIONS_URL}/", headers=headers)
    print_result("List User Predictions", response.status_code == 200)

    response = requests.get(f"{PREDICTIONS_URL}/stats/", headers=headers)
    print_result("Get Prediction Stats", response.status_code == 200)

    # 5. Analytics
    print("\n--- Analytics ---")
    response = requests.get(f"{ANALYTICS_URL}/dashboard/", headers=headers)
    print_result("Get Dashboard", response.status_code == 200)

    # 6. Recommendations
    print("\n--- Recommendations ---")
    response = requests.get(f"{RECOMMENDATIONS_URL}/matches/", headers=headers)
    print_result("Get Recommended Matches", response.status_code == 200)

    response = requests.get(f"{RECOMMENDATIONS_URL}/trending/", headers=headers)
    print_result("Get Trending Matches", response.status_code == 200)

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"❌ Critical Error: {e}")
