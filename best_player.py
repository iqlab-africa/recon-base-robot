import json
import os
import random
import requests
from robocorp.tasks import task
from robocorp import workitems
from datetime import datetime
import pandas as pd
import random

from webhook import send_webhook

#
PREFIX = "https://autofunctionapp.azurewebsites.net/api/"
BEST_PLAYER = f"{PREFIX}bestplayer"

tag3 = "🌸 🌸 🌸 🌸 BestPlayerRobot 🍎 "

os.environ["RC_WORKITEM_ADAPTER"] = "FileAdapter"
os.environ["RC_WORKITEM_INPUT_PATH"] = "devdata/input_to_best_player/work-items.json"
os.environ["RC_WORKITEM_OUTPUT_PATH"] = "output/bestplayer/work-items.json"


@task
def best_player_task():
    """Process the selected player from the PlayerHandlerRobot"""
    print(
        f"\n\n{tag3} start processing best player from PlayerHandlerRobot workitem ..."
    )
    
    curr = workitems.inputs.current
    name = ''
    try:
        name = curr.payload["name"]
        print(f"\n{tag3} ... 🥬🥬🥬🥬🥬 Processing Best Player: {name}")
        curr.done()
    except Exception as e:
        print(f"{tag3} Error processing player: {e}")

    print(f"\n\n{tag3} ... 1 workitem processed; calling webhook: 🔵 {BEST_PLAYER}")
    
    robot_name = "BestPlayerRobot";
    send_webhook(robotName=robot_name, processed=1, emoji="🔵")
    send_best_player(robotName=robot_name, player=name)


def send_best_player(robotName: str, player: str):
    data = {
        "robotName": robotName,
        "bestPlayer": player,
        "robotDate": datetime.now().ctime(),
    }
    json_object = json.dumps(data)
    print(f"\n{tag3} 🔵 🔵 🔵  sending data to BestPlayerFunction: {json_object}")
    res = requests.post(
        url=BEST_PLAYER,
        data=json_object,
    )
    print(
        f"\n{tag3} ✅ ✅ robotName: {robotName} BestPlayerFunction response, 🥬 status_code: {res.status_code} - {res.text}\n\n "
    )
