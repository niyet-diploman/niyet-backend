from enum import IntEnum


class Roles(IntEnum):
    ADMIN = 1
    MANAGER = 2
    USER = 3
    MANAGER_REGION = 4
    PARTNER = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
