import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = "https://robot-keys-2.vault.azure.net/"


def get_virtual_machine_connection_string():
    return get_key(vault_url=vault_url, key_name="connection")


def get_database_connection_string():

    return get_key(vault_url=vault_url, key_name="database-connection-json")


def get_json_key():
    return get_key(vault_url=vault_url, key_name="json")


def get_key(key_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    secret: SecretClient
    try:
        secret = client.get_secret(name=key_name)
        return secret.value

    except Exception as e:
        print(f"👿👿👿👿👿 ERROR getting connection string: {e} 👿")
    raise KeyError(f"Unable to find key: {key_name}")


# Using the special variable
if __name__ == "__main__":
    secret_key = get_virtual_machine_connection_string()
    json_key = get_json_key()
    database_string = get_database_connection_string()

    print(
        f"\n🍎🍎🍎 #1 we good, Boss! virtual machine connection string : \n{secret_key} 🥬\n"
    )
    print(f"\n🍎🍎🍎 #2 we good, Boss! example json string : \n{json_key} 🥬\n\n")
    print(
        f"\n🍐🍐🍐 #3 we good, Boss! database connection json string : \n{database_string} 🥬\n"
    )

    m = json.loads(s=json_key)
    username = m.get("userName")
    password = m.get("password")
    module = m.get("module")

    print(f"🔵 username : {username} 🔵 password: {password} 🔵 module: {module} \n")

    x = json.loads(s=database_string)
    user = x.get("user")
    password2 = x.get("password")
    dbname = x.get("dbname")
    host = x.get("host")

    print(
        f"🔴 user : {user} 🔴 password: {password2} 🔴 dbname: {dbname} 🔴 host: {host}\n\n"
    )
