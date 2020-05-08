from Exceptions import EventExists
from models.Event import Event
from services import db

events = db.get_collection("events")


def new_event(event: Event):
    if events.find_one({"name": event.name}) is not None:
        raise EventExists

    events.insert_one(event.__dict__)
    return "Event Inserted Successfully!"


def all_events(uid):
    return events.find({"paid_by": uid}, projection={"_id": 0})


def contact_owe(uid):
    user_events = all_events(uid)
    contact_to_money = {}
    for event in user_events:
        money_owed = int(event["amount"] / (len(event["users"])+1))
        for user in event["users"]:
            if user in contact_to_money:
                contact_to_money[user] += money_owed
            else:
                contact_to_money[user] = money_owed
    return contact_to_money
