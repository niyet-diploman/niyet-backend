from enum import IntEnum


class BeneficiariesDonationState(IntEnum):
    AVAILABLE = 1
    IN_PROCESS = 2
    PENDING_PAYMENT = 3
    LOCKED = 4

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DonationState(IntEnum):
    PAYED = 1
    PENDING = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BeneficiariesGenderStatus(IntEnum):
    BOY = 1
    GIRL = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BeneficiariesSocialStatus(IntEnum):
    CHILDREN_WITH_SPECIAL_NEEDS = 1
    ORPHAN = 2
    LARGE_FAMILY = 3
    LOW_INCOME_FAMILY = 4
    DISABLED = 5
    NIET_FUND = 6

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class BeneficiariesAnonymStatus(IntEnum):
    PUBLIC = 1
    ANONYM = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DonationType(IntEnum):
    COMMON = 1
    ZAKYAT = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DonorAnonymStatus(IntEnum):
    ANONYM = 1
    PUBLIC = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class DonorRecurringPeriod(IntEnum):
    WEEK = 1
    MONTH = 2
    QUARTER = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class IssuerType(IntEnum):
    INDIVIDUAL = 1
    LEGAL_ENTITY = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class IssueState(IntEnum):
    CREATED = 1
    GIVEN = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PaymentStatus(IntEnum):
    CREATED_PAYMENT = 1
    PAYMENT_PENDING_PAYBOX = 2
    PAYMENT_EXPIRED = 3
    PAYMENT_PAYED = 4
    SYSTEM_ERROR = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
