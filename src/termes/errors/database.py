class DatabaseError(Exception):
    pass


class ItemNotFoundError(DatabaseError):
    pass
