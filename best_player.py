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
PING_URL = f"{PREFIX}ping"
DEV_ADD_USER_URL = f"{PREFIX}adddevuser"
DEV_LIST_USERS = f"{PREFIX}listdevusers"
BEST_PLAYER = f"{PREFIX}bestplayer"
DOWNLOAD = f"{PREFIX}download"

CSV_FILE_NAME = "football_players.csv"
CSV_OUTPUT_FILE_PATH = "output/players.csv"

tag3 = "🌸 🌸 🌸 🌸 BestPlayerRobot 🍎 "
os.environ["RC_WORKITEM_ADAPTER"] = "FileAdapter"
os.environ["RC_WORKITEM_INPUT_PATH"] = "devdata/my_input2/work-items.json"


@task
def best_player_task():
    """Process the selected player from the PlayerHandlerRobot"""
    print(
        f"\n\n{tag3}... start processing best player from PlayerHandlerRobot workitems ..."
    )
    if workitems.inputs:
        print(f"{tag3} We have inputs .... {workitems.inputs}")
    else:
        print(f"{tag3} We have NO inputs .... {workitems.inputs}")

    curr = workitems.inputs.current
    name = ''
    try:
        name = curr.payload["name"]
        print(f"{tag3} ... 🥬🥬🥬🥬🥬 Processing prize winner: {name}")
        curr.done()
    except Exception as e:
        print(f"{tag3} Error processing player: {e}")

    print(f"\n\n{tag3} ... 1 workitem processed; calling webhook: 🔵 {BEST_PLAYER}")
    robot_name = "BestPlayerRobot";
    send_webhook(robotName=name, processed=1, emoji="🔵")
    send_best_player(robotName=robot_name, player=name)


def send_best_player(robotName: str, player: str):
    data = {
        "robotName": robotName,
        "bestPlayer": player,
        "robotDate": datetime.now().ctime(),
    }
    json_object = json.dumps(data)
    print(f"\n🔵 🔵 🔵  send data to BestPlayerFunction: {json_object}")
    res = requests.post(
        url=BEST_PLAYER,
        data=json_object,
    )
    print(
        f"\n✅ ✅ robotName: {robotName} BestPlayerFunction response, 🥬 status_code: {res.status_code} - {res.text}\n\n "
    )
