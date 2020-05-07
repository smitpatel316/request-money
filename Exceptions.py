from pymongo.errors import PyMongoError


class UserExists(PyMongoError):
    pass


class EventExists(PyMongoError):
    pass


class UserNotFound(PyMongoError):
    pass
