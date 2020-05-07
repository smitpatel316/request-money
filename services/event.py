from Exceptions import EventExists
from models.Event import Event
from services import db

events = db.get_collection("events")


def new_event(event: Event):
    if events.find_one({"name": event.name}) is not None:
        raise EventExists

    events.insert_one(event.__dict__)
    return "Event Inserted Successfully!"
