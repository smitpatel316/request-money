from flask import Blueprint, request

from Exceptions import UserExists
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
            registration_id=new_user_data.get("registrationId")
        )
        if "secretKey" in new_user_data:
            new_user.set_secret_key(new_user_data.get("secretKey"))
        return user_service.add_new_user(new_user)

    except UserExists:
        return "User already exists in the database with same name and email.", 409

    except Exception as e:
        return str(e), 500
