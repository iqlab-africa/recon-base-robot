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

CSV_FILE_NAME = "football_players.csv"
CSV_OUTPUT_FILE_PATH = "output/players.csv"

tag2 = "🍎 🍎 PlayerHandlerRobot 🍎 "
os.environ["RC_WORKITEM_ADAPTER"] = "FileAdapter"
os.environ['RC_WORKITEM_INPUT_PATH'] = 'devdata/input_to_player_handler/work-items.json'
os.environ["RC_WORKITEM_OUTPUT_PATH"] = 'output/handler/work-items.json'


@task
def player_handler_task():
    """Process the input Work Items from the previous step."""
    print(f"\n\n{tag2} start processing names from PlayerCollectorRobot workitem ...")

    best_player = 'NOT SELECTED YET!'

    best_player, work_item = handle_work_item()
    create_work_item(best_player)
    work_item.done()
    
    # Tell someone!
    send_webhook(robotName="PlayerHandlerRobot", processed=1, emoji="🍎")
    print(
        f"{tag2} 🔵 Best Player: {best_player} 🔵 The PlayerHandlerRobot's work is done, Boss! 🥬\n\n"
    )

def handle_work_item():
    work_item = workitems.inputs.current

    try:        
        if work_item:
            print(f'{tag2} handling input workitem ... ')
            payload = work_item.payload['players']
            print(f'{tag2} workitem payload has {len(payload)} players')
            best_player = random.choice(payload)
            print(f'{tag2} Best Player randomly selected: {best_player}')

    except Exception as e:
        print(f"{tag2} we have a problem, Jack! : {e}")
        
    return best_player, work_item


def create_work_item(player):
    try:
        data = {"name": player}
        workitems.outputs.create(payload=data)
        print(f"\n{tag2} 🌕 🌕 🌕 created an output workitem for BestPlayerRobot: 🌺 {data} 🌺\n")
    except Exception as e:
        print(f"{tag2} 😈 😈 😈 ERROR generating workitem {e}")
