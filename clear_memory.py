import os
import urllib.request
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("HINDSIGHT_BASE_URL")
api_key = os.getenv("HINDSIGHT_API_KEY")
bank_id = os.getenv("HINDSIGHT_BANK_ID")

url = f"{base_url}/v1/default/banks/{bank_id}/memories"

request = urllib.request.Request(
    url,
    method="DELETE",
    headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    },
)

with urllib.request.urlopen(request) as response:
    result = response.read().decode()

print("✅ Hindsight memory bank cleared!")
print(result)