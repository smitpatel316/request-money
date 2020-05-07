import requests
from bson import ObjectId
from bson.json_util import dumps

from Exceptions import UserExists, UserNotFound
from models.Contact import Contact
from models.User import User
from services import db

users = db.get_collection(name="users")
ENDPOINT_ADDRESS_V2 = "https://gateway-web.beta.interac.ca/publicapi/api/v2"
CONTACT_ENDPOINT = "/contacts"


def add_new_user(user: User):
    if users.find_one({"name": user.name, "email": user.email}) is not None:
        raise UserExists
    users.insert_one(user.to_dict())
    return "User Inserted Successfully!"


def get_all_users():
    return dumps(users.find(projection={"name": 1, "email": 1}))


def find_user(uid):
    user = users.find_one({"_id": ObjectId(uid)})
    if user is None:
        raise UserNotFound
    return user


def add_new_contact(user, contact: Contact):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "thirdPartyAccessId": user.get("third_party_access_id"),
        "accessToken": f"Bearer {user.get('access_token')}",
        "apiRegistrationId": user.get("registration_id"),
        "requestId": "test123",
        "deviceId": "test123",
    }
    body = {
        "contactName": contact.name,
        "language": "en",
        "notificationPreferences": [
            {
                "handle": contact.handle,
                "handleType": contact.handle_type,
                "active": True,
            }
        ],
    }
    res = requests.post(
        url=f"{ENDPOINT_ADDRESS_V2}{CONTACT_ENDPOINT}", headers=headers, json=body,
    )
    res.raise_for_status()

    contact.set_id(res.json().get("contactId"))
    contact.set_hash(res.json().get("contactHash"))

    user["contacts"].append(contact.__dict__)
    users.find_one_and_update(
        {"_id": ObjectId(user.get("_id"))}, {"$set": {"contacts": user.get("contacts")}}
    )
    return "Added new contact!"
