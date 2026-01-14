import requests
import time

BASE_URL = "http://localhost:8001/api"

def test_flow():
    print("1. Generating a new login code...")
    gen_resp = requests.post(f"{BASE_URL}/admin/generate-code", json={"candidate_name": "John Doe"})
    if gen_resp.status_code != 200:
        print(f"Failed to generate code: {gen_resp.text}")
        return
    
    data = gen_resp.json()
    code = data["code"]
    print(f"Generated code: {code}")

    print("\n2. Validating the code for the first time...")
    val_resp = requests.post(f"{BASE_URL}/validate-code", json={"code": code})
    val_data = val_resp.json()
    print(f"Validation result: {val_data}")
    if not val_data["valid"]:
        print("Error: Code should be valid!")
        return

    print("\n3. Validating the same code again...")
    val_resp2 = requests.post(f"{BASE_URL}/validate-code", json={"code": code})
    val_data2 = val_resp2.json()
    print(f"Validation result: {val_data2}")
    if val_data2["valid"]:
        print("Error: Code should be invalid (already used)!")
        return
    print("Success: Code rejected as expected.")

    print("\n4. Validating a non-existent code...")
    val_resp3 = requests.post(f"{BASE_URL}/validate-code", json={"code": "INVALID123"})
    val_data3 = val_resp3.json()
    print(f"Validation result: {val_data3}")
    if val_data3["valid"]:
        print("Error: Non-existent code should be invalid!")
        return
    print("Success: Non-existent code rejected as expected.")

if __name__ == "__main__":
    try:
        test_flow()
    except Exception as e:
        print(f"An error occurred: {e}")
