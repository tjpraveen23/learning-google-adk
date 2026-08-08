"""
Test FastAPI Streaming Endpoint
Run: python testcases/test_fastapi.py
"""

import json
import requests

API_URL = "http://127.0.0.1:8000/travel"

payload = {
    "prompt": "Plan a Chennai trip under 20000",
    "user_id": "praveen_tj",
}

print("Connecting to FastAPI...")

response = requests.post(
    API_URL,
    json=payload,
    stream=True,
    headers={
        "Accept": "text/event-stream"
    },
)

if response.status_code != 200:
    print(response.status_code)
    print(response.text)
    raise SystemExit(1)

print("Streaming response...")
print("-" * 60)

buffer = ""

for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):

    if not chunk:
        continue

    buffer += chunk

    while "\\n\\n" in buffer:

        event_text, buffer = buffer.split("\\n\\n", 1)

        if not event_text.startswith("data: "):
            continue

        json_text = event_text[6:].strip()

        try:
            event = json.loads(json_text)
        except json.JSONDecodeError:
            print("Invalid JSON:")
            print(json_text)
            continue

        print(
            f"[{event.get('agent')}] "
            f"{event.get('status')} - "
            f"{event.get('message')}"
        )

        if event.get("agent") == "Final":
            print()
            print("Performance:")
            print(event.get("performance"))

print()
print("Streaming completed.")