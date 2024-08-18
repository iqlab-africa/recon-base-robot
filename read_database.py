import json
import requests


PREFIX = "https://autofunctionapp.azurewebsites.net/api/"
WEB_HOOKS = f"{PREFIX}webhooklist"
BEST_PLAYERS = f"{PREFIX}bestplayerlist"

tag = "🌿🌿🌿🌿 DatabaseReader 🍎 "


def read_web_hooks():
    """Get webhooks to show that robots ran and saved data in Postgres"""
    print(f"\n{tag} calling {WEB_HOOKS}")

    res = requests.get(WEB_HOOKS)
    if res.status_code == 200:
        print(f"{tag} read_web_hooks: status code: {res.status_code}")
        m_json = json.loads(res.text)
        for j in m_json:
            print(f"{tag} Robot date: {j['robotDate'].strip()}  🔵 {j['robotName'].strip()}")

        print(f"\n{tag} Robot WebHooks found: {len(m_json)}")


def read_best_players():
    """Get best players to show that result of work done by the last step of the Robot run"""
    print(f"\n\n{tag} calling {BEST_PLAYERS}")
    res = requests.get(BEST_PLAYERS)
    if res.status_code == 200:
        print(f"{tag} read_best_players: status code: {res.status_code}")
        m_json = json.loads(res.text)
        for j in m_json:
            print(
                f"{tag} {j['robotDate'].strip()} 🥬 Player: {j['bestPlayer'].strip()}"
            )

        print(f"\n{tag} Best Players found: {len(m_json)}")


def start_reading_database():
    print(f'\n\n{tag} read Azure Postgres database to see data produced by Robots running')
    read_web_hooks()
    read_best_players()
    print('\n\n')


#start_reading_database()
