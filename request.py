import requests

BASE_URL = "http://127.0.0.1:8000"

# 1) login with HTTP Basic
resp = requests.post(f"{BASE_URL}/login", auth=("dev_user", "dev_user"))
resp.raise_for_status()
token = resp.json()["access_token"]

# 2) call protected with Bearer token
headers = {"Authorization": f"Bearer {token}"}
resp2 = requests.get(f"{BASE_URL}/protected", headers=headers)
print(resp2.status_code, resp2.json())

