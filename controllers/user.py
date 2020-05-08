from flask import Blueprint, request

from Exceptions import UserExists, UserNotFound
from models.Contact import Contact
from models.User import User
from services import user as user_service

user = Blueprint(name="user", import_name=__name__, url_prefix="/api/v1/user")


@user.route("/")
def all_users():
    return user_service.get_all_users()


@user.route("/add", methods=["POST"])
def add_user():
    new_user_data: dict = request.json
    for field in ["name", "email", "thirdPartyAccessId", "registrationId"]:
        if field not in new_user_data:
            return f"Missing field {field} in Request body", 400
    try:
        new_user = User(
            name=new_user_data.get("name"),
            email=new_user_data.get("email"),
            third_party_access_id=new_user_data.get("thirdPartyAccessId"),
            registration_id=new_user_data.get("registrationId"),
        )
        if "secretKey" in new_user_data:
            new_user.set_secret_key(new_user_data.get("secretKey"))
        return user_service.add_new_user(new_user)

    except UserExists:
        return "User already exists in the database with same name and email.", 409

    except Exception as e:
        return str(e), 500


@user.route("/contact", methods=["POST"])
def new_contact():
    new_contact_data: dict = request.json
    for field in ["name", "handleType", "handle", "uid"]:
        if field not in new_contact_data:
            return f"Missing field {field} in Request body", 400
    try:
        found_user = user_service.find_user(new_contact_data.get("uid"))
        contact = Contact(
            name=new_contact_data.get("name"),
            handle=new_contact_data.get("handle"),
            handle_type=new_contact_data.get("handleType"),
        )

        return user_service.add_new_contact(user=found_user, contact=contact)

    except UserNotFound:
        return "User does not exists in the database.", 409

    except Exception as e:
        return str(e), 500


@user.route("/contacts/<uid>")
def get_all_contacts(uid):
    return user_service.get_all_contacts(uid)


@user.route("/request-money", methods=["POST"])
def bulk_money_request():
    body = request.json
    for field in ["uid", "contacts"]:
        if field not in body:
            return f"Field {field} missing from body", 400
    return {"message": user_service.bulk_money_request(body.get("uid"), body.get("contacts"))}


@user.route("/test")
def test():
    return user_service.send_money_request(user_service.find_user("5eb45480a6f04c792cb73bdd"),
                                           contact_id="CAFmzkZfxEF4",
                                           contact_hash="058daae2fad4531b228a5f542da091a5",
                                           amount=47)
