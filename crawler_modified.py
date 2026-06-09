import requests
from bs4 import BeautifulSoup
import sys

TOKEN_WORDS = ["csrf", "_token", "xsrf"]

url = sys.argv[1]

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

forms = soup.find_all("form")

protected = 0
vulnerable = 0

for form in forms:
    method = (form.get("method") or "GET").upper()

    if method != "POST":
        continue

    has_token = False

    for field in form.find_all("input"):
        name = (field.get("name") or "").lower()

        if any(word in name for word in TOKEN_WORDS):
            has_token = True

    if has_token:
        protected += 1
        print("[SAFE] POST form contains CSRF token")
    else:
        vulnerable += 1
        print("[HIGH RISK] POST form missing CSRF token")

print("\\n--- Scan Summary ---")
print("Protected Forms:", protected)
print("Vulnerable Forms:", vulnerable)
