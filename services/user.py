from Exceptions import UserExists

from models.User import User
from bson.json_util import dumps
from services import db

users = db.get_collection(name="users")


def add_new_user(user: User):
    if users.find_one({"name": user.name, "email": user.email}) is not None:
        raise UserExists
    users.insert_one(user.__dict__)
    return "User Inserted Successfully!"


def get_all_users():
    return dumps(users.find(projection={"name": 1, "email": 1}))
