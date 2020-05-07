import base64
import hashlib
import secrets

import requests

from models.Contact import Contact

ENDPOINT_ADDRESS_V1 = "https://gateway-web.beta.interac.ca/publicapi/api/v1"
ENDPOINT_ADDRESS_V2 = "https://gateway-web.beta.interac.ca/publicapi/api/v2"
ACCESS_TOKEN_ENDPOINT = "/access-tokens"
CONTACT_ENDPOINT = "/contacts"
REQUEST_MONEY_ENDPOINT = "/money-requests/send"


class User:
    def __init__(
            self, name, email, third_party_access_id, registration_id=None, secret_key=None
    ):
        self.name = name
        self.email = email
        self.third_party_access_id = third_party_access_id
        self.registration_id = registration_id
        self.secret_key = secret_key
        self.encrypted_key = None
        self.access_token = None
        self.salt = secrets.token_hex(16)
        if self.secret_key is not None:
            self.generate_encrypted_key()
            self.generate_access_token()

        self.contacts: [Contact] = []

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key
        self.generate_encrypted_key()
        self.generate_access_token()

    def set_registration_id(self, registration_id):
        self.registration_id = registration_id

    def generate_encrypted_key(self):
        if self.secret_key is None:
            raise Exception("Generating Encrypted Key: Secret Key is not yet set.")
        hashed = hashlib.sha256(f"{self.salt}:{self.secret_key}".encode())
        encoded = base64.b64encode(hashed.digest())
        self.encrypted_key = encoded.decode()

    def generate_access_token(self):
        if self.encrypted_key is None:
            self.encrypted_key = self.generate_encrypted_key()
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "thirdPartyAccessId": self.third_party_access_id,
            "salt": self.salt,
            "secretKey": self.encrypted_key,
        }
        res = requests.get(
            url=f"{ENDPOINT_ADDRESS_V1}{ACCESS_TOKEN_ENDPOINT}", headers=headers
        )
        if res.status_code not in [200, 201]:
            res.raise_for_status()
        self.access_token = res.json().get("access_token")

    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "third_party_access_id": self.third_party_access_id,
            "registration_id": self.registration_id,
            "secret_key": self.secret_key,
            "encrypted_key": self.encrypted_key,
            "access_token": self.access_token,
            "salt": self.salt,
            "contacts": [contact.__dict__ for contact in self.contacts],
        }
