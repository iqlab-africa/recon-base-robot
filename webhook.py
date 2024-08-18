from datetime import datetime
import json

import requests
WEBHOOK = "https://autofunctionapp.azurewebsites.net/api/webhook"


def send_webhook(robotName: str, emoji: str, processed: int):
    data = {
        "robotName": robotName,
        "processed": processed,
        "robotDate": datetime.now().ctime(),
        "emoji": emoji,
    }
    json_object = json.dumps(data)
    print(f"\n🔵 🔵 🔵  send data to webhook: {json_object}")
    res = requests.post(
        url=WEBHOOK,
        data=json_object,
    )
    print(
        f"\n✅ ✅ robotName: {robotName} webhook response, 🥬 status_code: {res.status_code} - {res.text}\n\n "
    )
