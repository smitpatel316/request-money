import secrets

import requests
from bson import ObjectId
from bson.json_util import dumps

from Exceptions import UserExists, UserNotFound
from models.Contact import Contact
from models.User import User
from services import db
from services.event import contact_owe

users = db.get_collection(name="users")
ENDPOINT_ADDRESS_V2 = "https://gateway-web.beta.interac.ca/publicapi/api/v2"
REQUEST_MONEY_ENDPOINT = "/money-requests/send"
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
        url=f"{ENDPOINT_ADDRESS_V2}{CONTACT_ENDPOINT}", headers=headers, json=body
    )
    res.raise_for_status()

    contact.set_id(res.json().get("contactId"))
    contact.set_hash(res.json().get("contactHash"))

    user["contacts"].append(contact.__dict__)
    users.find_one_and_update(
        {"_id": ObjectId(user.get("_id"))}, {"$set": {"contacts": user.get("contacts")}}
    )
    return "Added new contact!"


def get_all_contacts(uid):
    return dumps(
        users.find({"_id": ObjectId(uid)}, projection={"contacts": 1, "_id": 0})[0][
            "contacts"
        ]
    )


def bulk_money_request(uid, contacts):
    user = find_user(uid)
    print(user)
    for contact in contacts:
        send_money_request(user, contact.get("id"), contact.get("hash"), contact.get("amount"))
    return "Bulk Money Request Successful!"


def send_money_request(user, contact_id, contact_hash, amount):
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
        "sourceMoneyRequestId": secrets.token_hex(16),
        "requestedFrom": {
            "contactId": contact_id,
            "contactHash": contact_hash
        },
        "amount": amount,
        "currency": "CAD",
        "editableFulfillAmount": False,
        "expiryDate": "2020-08-28T16:12:12.721Z",
        "supressResponderNotifications": False
    }
    res = requests.post(url=f"{ENDPOINT_ADDRESS_V2}{REQUEST_MONEY_ENDPOINT}", headers=headers, json=body)
    res.raise_for_status()
    return "Money Request Sent"
