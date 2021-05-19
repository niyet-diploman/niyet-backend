from enum import IntEnum


class PostType(IntEnum):
    NEWS = 1
    STORIES = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class QuestionStatus(IntEnum):
    NEW = 1
    IN_PROCESS = 2
    CLOSED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

