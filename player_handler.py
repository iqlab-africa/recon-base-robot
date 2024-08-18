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
WEBHOOK = f"{PREFIX}webhook"

CSV_FILE_NAME = "footbal_players.csv"
CSV_OUTPUT_FILE_PATH = "output/players.csv"

tag2 = "🍎 🍎 PlayerHandlerRobot 🍎 "
os.environ["RC_WORKITEM_ADAPTER"] = "FileAdapter"
os.environ['RC_WORKITEM_INPUT_PATH'] = 'devdata/my_input/work-items.json'

@task
def player_handler_task():
    """Process all the produced input Work Items from the previous step."""
    print(f"\n\n{tag2}... start processing names from workitems ...")

    if workitems.inputs:
        print(f'{tag2} We have inputs .... {workitems.inputs}')
    else:
        print(f"{tag2} We have NO inputs .... {workitems.inputs}")

    names = []
    count = 0
    done = False
    random_name = ''
    try:        
        # for item in workitems.inputs:
        #     names.append(item.payload["name"])
        # print(f'{tag2} names {len(names)}')
        # random_name = random.choice(names)
        # print(f'{tag2} random name: {random_name}')
        for item in workitems.inputs:
            try:
                name = item.payload["name"]
                if done is False:
                    random_number = random.randint(1, 100)
                    print(random_number)
                    if random_number > 70:
                        print(f"\n{tag2} randomly chosen number: {random_number}")
                        create_work_item(item=name)
                        done = True

                names.append(name)
                print(f"{tag2} ... Processing name: {name}")
                # item.done()
                count = count + 1
            except Exception as e:
                print(f"{tag2} Error processing name: {e}")
                continue
    except Exception as e:
        print(f"{tag2} we have a problem, Jack! : {e}")

    # Tell someone!
    print(f"\n\n{tag2} ... {count} workitems processed; calling webhook: 🔵 {WEBHOOK}")
    send_webhook(robotName="PlayerHandlerRobot", processed=count, emoji="🍎")

    # Assuming names list is populated with some values
    # if len(names) > 0:
    #     random_name = random.choice(names)
    #     print(f"{tag2} randomly chosen player: {random_name}")
    # create_work_item(random_name)

def create_work_item(item):
    try:
        workitems.outputs.create(payload={"name": item})
        print(f"\n{tag2} 🌕 randomly chosen player created a workitem: 🌺 {item} 🌺\n")
    except Exception as e:
        print(f'{tag2} ERROR {e}')


def handle_transaction(data):
    print(f'{tag2} ... data : {data.get("name")}')


def check_valid_id(value):
    if len(value) < 8:
        raise workitems.BusinessException(
            code="INVALID_ID",
            message="Transaction ID length is too short!",
        )


#
def process_traffic_data():
    for item in workitems.inputs:
        traffic_data = item.payload["traffic_data"]
        if len(traffic_data["country"]) == 3:
            status, return_json = 200
            if status == 200:
                item.done()
            else:
                item.fail(
                    exception_type="APPLICATION",
                    code="TRAFFIC_DATA_POST_FAILED",
                    message=return_json["message"],
                )
        else:
            item.fail(
                exception_type="BUSINESS",
                code="INVALID_TRAFFIC_DATA",
                message=item.payload,
            )
