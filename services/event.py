from bson import ObjectId

from Exceptions import EventExists
from models.Event import Event
from services import db

events = db.get_collection("events")


def new_event(event: Event):
    if events.find_one({"name": event.name}) is not None:
        raise EventExists

    events.insert_one(event.__dict__)
    return {"message": "Event Inserted Successfully!"}


def all_events(uid):
    return events.find({"paid_by": uid}, projection={"_id": 0})


def contact_owe(uid):
    user_events = all_events(uid)
    contact_to_money = {}
    for event in user_events:
        money_owed = int(event["amount"] / event["number_of_users"])
        for user in event["users"]:
            if user in contact_to_money:
                contact_to_money[user] += money_owed
            else:
                contact_to_money[user] = money_owed
    return contact_to_money


def remove_event(_id):
    if isinstance(_id, str):
        _id = ObjectId(_id)
    events.remove({"_id": _id})


def get_events_for_contact(contact_hash: str):
    return events.find({"users": contact_hash})


def remove_user(contact_hash: str):
    contact_events = get_events_for_contact(contact_hash)
    for event in contact_events:
        event["users"].remove(contact_hash)
        if len(event["users"]) == 0:
            remove_event(event["_id"])
        else:
            _id = event["_id"]
            if isinstance(_id, str):
                _id = ObjectId(_id)
            events.update({"_id": _id}, event)