import json
import os
import random
import requests
from robocorp.tasks import task
from robocorp import workitems
from datetime import datetime
import pandas as pd
import random
from azure.storage.blob import BlobServiceClient

from webhook import send_webhook

#
PING_URL = "https://autofunctionapp.azurewebsites.net/api/ping"
DEV_ADD_USER_URL = "https://autofunctionapp.azurewebsites.net/api/adddevuser"
DEV_LIST_USERS = "https://autofunctionapp.azurewebsites.net/api/listdevusers"
WEBHOOK = "https://autofunctionapp.azurewebsites.net/api/webhook"
DOWNLOAD = "https://autofunctionapp.azurewebsites.net/api/download"

os.environ["RC_WORKITEM_OUTPUT_PATH"] = "output/collector/work-items.json"

CSV_FILE_NAME = "football_players.csv"
CSV_OUTPUT_FILE_PATH = "output/players.csv"
tag = "🍐🍐 PlayerCollectorRobot 🍐 "


@task
def player_collector_task():
    """Demonstrate connection to Azure Functions and Postgres database. Read the code to see the different api's"""
    print(f"\n\n{tag} PlayerCollectorRobot starting ...")
    # ping()
    # add_user()
    # get_users()
    download_player_file_from_azure()
    #
    send_webhook(robotName="PlayerCollectorRobot", processed=1, emoji="🥬")
    print(f"\n\n{tag} Work is done, Jackson!  🥬 \n\n")

def ping():
    """Ping Azure Functions"""
    print(f"\n... 💙 💙 💙 calling {PING_URL}")
    res = requests.get(url=PING_URL)
    print(f"🔴 🔴 Ping response, 🥬 status_code: {res.status_code} \n{res.text}\n\n ")

def add_user():
    """Call Azure function to add dev user"""
    print(f"\n... 💙 💙 💙 calling {DEV_ADD_USER_URL}")

    try:
        name = f"Player #{random.random()}"
        data = {"name": name}
        json_object = json.dumps(data)
        res = requests.post(
            url=DEV_ADD_USER_URL,
            data=json_object,
        )
        print(
            f"✅ ✅ add_user response, 🥬 status_code: {res.status_code} \n{res.text}\n\n "
        )
    except Exception as e:
        print(f"Error adding user: 😈 {e} 😈")

def get_users():
    """Call Azure function to list dev users"""
    print(f"\n... 💙 💙 💙 calling {DEV_LIST_USERS}")

    try:
        res = requests.get(url=DEV_LIST_USERS)
        print(f"🍐 🍐 get_users response, 🥬 status_code: {res.status_code} \n")
        m_json = json.loads(res.text)
        print(
            f"\n🍐 🍐 get_users response, 🥬 status_code: {res.status_code} users:{len(m_json)}\n\n "
        )
    except Exception as e:
        print(f"😈 Error listing users: 😈 {e} 😈")

def download_player_file_from_azure():
    """Download files from Azure Storage account. download both excel and csv versions and create dataFrames"""

    player_list = []
    csv_data_frame: pd.DataFrame = _download(CSV_FILE_NAME)
    if csv_data_frame is not None:
        player_list = _print_data_frame(csv_data_frame)

    if len(player_list) > 0:
        create_work_item(player_list)
    else:
        print(
            f"\n{tag} 👿 download stumbled, grumbled and fell down!, no workitems will be created! 👿👿👿\n"
        )

def _print_data_frame(df: pd.DataFrame) -> list:

    print(f"{tag} head: {df.head()}\n")
    print(f"{tag} tail: {df.tail()}\n\n")

    player_list = df.iloc[1:, 0].astype(str).tolist()
    print(f"{tag} player list heading to workitems: 🍑 {player_list} 🍑\n")
    print(f"{tag} Number of players from file: {len(player_list)}\n")
    return player_list

def _download(fileName):
    """Download the file from Azure Storage via Azure Function api call"""
    ext = fileName.split(".")[-1]
    if not ext == "csv":
        raise ValueError("Only file types .csv is allowed")

    print(f"{tag} downloading {fileName} to {DOWNLOAD}...")
    # call the Function api
    try:
        data = {"fileName": fileName}
        json_data = json.dumps(data)
        print(f"{tag} json_data {json_data} ...")

        response = requests.post(url=DOWNLOAD, data=json_data)
        print(
            f"{tag} response status: {response.status_code} reason: {response.reason} headers: {response.headers}"
        )
        if response.status_code == 200:
            downloaded = response.text
        else:
            # raise ValueError("👿 Download failed")
            return

        print(
            f"\n{tag} Azure Storage file downloaded: 😡 😡 {len(downloaded)} bytes 😡\n"
        )

        with open(CSV_OUTPUT_FILE_PATH, "wb") as f:
            f.write(downloaded.encode())
        df = pd.read_csv(CSV_OUTPUT_FILE_PATH, header=None)

        return df

    except Exception as e:
        print(f"{tag} ERROR downloading file: {fileName}: {e}")
        raise ValueError(f"File download failed: {e}")

def create_work_item(names: list):
    """Send names to work items for the next robot"""
    print(f"{tag} sending {len(names)} names to workitems")
    count = 0
    data = {'players': names}
    workitems.outputs.create(data)
    print(f"\n\n{tag} ... {len(names)} items in workitem created; calling webhook: 🔵 {WEBHOOK}")
    send_webhook(robotName="PlayerCollectorRobot", processed=len(names), emoji="🍎")

    print(f"\n{tag} 🅿️  1 workitem created. Work completed, Boss! 🅿️")
