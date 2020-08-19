# security placeholders for app development testing
from werkzeug.security import safe_str_cmp
from user import User

# users = [
#     User(1, 'user1', 'abcxyz'),
# ]

# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}

def authenticate(username, password):
    # user = username_table.get(username, None)
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_table.get(user_id, None)
    return User.find_by_id(user_id)
