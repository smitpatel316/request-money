class Contact:
    def __init__(self, name, handle, handle_type):
        self.name = name
        self.handle = handle
        self.handle_type = handle_type
        self.id = None
        self.hash = None

    def set_id(self, contact_id):
        self.id = contact_id

    def set_hash(self, contact_hash):
        self.hash = contact_hash

    def __eq__(self, other):
        return self.name == other.name and self.handle == other.handle and self.handle_type == other.handle_type
