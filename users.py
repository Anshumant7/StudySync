import hashlib
import storage

def scramble_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def sign_up(username, password):
    all_users = storage.load_json(storage.USERS_FILE)

    if username in all_users:
        return False

    all_users[username] = scramble_password(password)
    storage.save_json(storage.USERS_FILE, all_users)
    return True

def log_in(username, password):
    all_users = storage.load_json(storage.USERS_FILE)

    if username not in all_users:
        return False

    return all_users[username] == scramble_password(password)