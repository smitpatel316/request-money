import requests
import secrets
import hashlib
import base64

ENDPOINT_ADDRESS = "https://gateway-web.beta.interac.ca/publicapi/api/v1"
ACCESS_TOKEN_ENDPOINT = "/access-tokens"


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

        self.contacts = []

    def set_secret_key(self, secret_key):
        self.secret_key = secret_key
        self.generate_encrypted_key()
        self.generate_access_token()

    def add_new_contact(self, contact):
        if contact not in self.contacts:
            self.contacts.append(contact)

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
            url=f"{ENDPOINT_ADDRESS}{ACCESS_TOKEN_ENDPOINT}", headers=headers
        )
        if res.status_code not in [200, 201]:
            res.raise_for_status()
        self.access_token = res.json().get("access_token")
