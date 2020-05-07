from flask import Blueprint, request

from Exceptions import EventExists
from models.Event import Event
from services import event as event_service

event = Blueprint(name="event", import_name=__name__, url_prefix="/api/v1/event")


@event.route("/add", methods=["POST"])
def add_new_event():
    new_event_data = request.json
    for field in ["name", "paidBy", "amount", "users"]:
        if field not in new_event_data:
            return f"Missing field {field} in Request body", 400
    try:
        new_event = Event(
            name=new_event_data.get("name"),
            paid_by=new_event_data.get("paidBy"),
            amount=new_event_data.get("amount"),
            users=new_event_data.get("users"),
        )
        return event_service.new_event(new_event)

    except EventExists:
        return "An event already exists with this name", 409

    except Exception as e:
        return str(e), 500
