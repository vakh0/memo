import json
from diarybook import Diary

def read_from_json_into_application(path, username):
    try:
        with open(path) as file:
            data = json.load(file)
        if not isinstance(data, dict):
            data = {}
        user_data = data.get(username, [])
        return [Diary(entry['memo'], entry['tags']) for entry in user_data]
    except FileNotFoundError:
        print(f"{path} not found. Creating a new one.")
        with open(path, 'w') as file:
            json.dump({}, file)
        return []
    except json.JSONDecodeError:
        print(f"{path} is malformed. Re-initializing.")
        with open(path, 'w') as file:
            json.dump({}, file)
        return []

def read_users_from_json(path):
    try:
        with open(path, 'r') as file:
            users = json.load(file)
            return users
    except FileNotFoundError:
        print("users.json not found. Creating a new one.")
        with open(path, 'w') as file:
            json.dump([], file)
        return []
    except json.JSONDecodeError:
        print("users.json is malformed. Re-initializing.")
        with open(path, 'w') as file:
            json.dump([], file)
        return []

def write_users_to_json(path, users):
    with open(path, 'w') as file:
        json.dump(users, file)

def write_diaries_to_json(path, username, diaries):
    try:
        with open(path, 'r') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    if not isinstance(data, dict):
        data = {}

    data[username] = [diary.to_dict() for diary in diaries]

    with open(path, 'w') as file:
        json.dump(data, file)
