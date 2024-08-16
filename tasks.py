import json
import random
from sqlite3 import Date
import requests
from robocorp.tasks import task
from datetime import datetime
from auth import get_database_connection_string, get_key
import pandas as pd

PING_URL = "https://autofunctionapp.azurewebsites.net/api/ping"
DEV_ADD_USER_URL = "https://autofunctionapp.azurewebsites.net/api/adddevuser"
DEV_LIST_USERS = "https://autofunctionapp.azurewebsites.net/api/listdevusers"

@task
def dev_robot_task():
    '''Demonstrate connection to Azure Functions and Postgres database'''
    ping()
    add_user()
    get_users()
    download_file_from_azure_storage('football_players.xlsx')


def ping():
    '''Ping Azure function'''
    print(f"\n... 💙 💙 💙 calling {PING_URL}")
    res = requests.get(url=PING_URL)
    print(f"🔴 🔴 Ping response, 🥬 status_code: {res.status_code} \n{res.text}\n\n ")

def add_user():
    '''Call Azure function to add dev user'''
    print(f"\n... 💙 💙 💙 calling {DEV_ADD_USER_URL}")

    try:
        name = f'Aubrey #{random.random()}'
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
        for m in m_json:
            print(f"🔶🔶 dev user: {m}")

        print(f"\n🍐 🍐 get_users response, 🥬 status_code: {res.status_code} users:{len(m_json)}\n\n ")
    except Exception as e:
        print(f"😈 Error listing users: 😈 {e} 😈")


from azure.storage.blob import BlobServiceClient

def download_file_from_azure_storage(blob_name):

    storage_key = get_key("storagekey")
    container_name = get_key("containername")
    account_name = get_key("accountname")
    print(
        f"🔆 account_name: {account_name} 🔆 container_name: {container_name} 🔆 account_key:{storage_key}"
    )
    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", 
                                            credential=storage_key)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    downloaded = blob_client.download_blob()
    with open(OUTPUT_FILE_PATH, "wb") as f:
        download_stream = downloaded
        f.write(download_stream.readall())
    print(f"🍐🍐🍐 Azure Storage file downloaded: {len(downloaded)} bytes")

    # check out the downloaded file
    df = pd.read_excel(OUTPUT_FILE_PATH)
    print(f"🍐🍐🍐 info: {df.info()}\n")
    print(f"🍐🍐🍐 describe: {df.describe()}\n")
    print(f"🍐🍐🍐 head: {df.head()}\n")
    print(f"🍐🍐🍐 tail: {df.tail()}\n\n")

OUTPUT_FILE_PATH = "output/players.xlsx"
