class Event:
    def __init__(self, name, users, paid_by, amount):
        self.name = name
        self.users = users
        self.paid_by = paid_by
        self.amount = amount
        self.number_of_users = len(users) + 1
