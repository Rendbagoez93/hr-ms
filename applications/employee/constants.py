from enum import StrEnum


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"

    @classmethod
    def choices(cls):
        return [(g.value, g.name.replace("_", " ").title()) for g in cls]


class EmergencyContactRelationship(StrEnum):
    SPOUSE = "spouse"
    PARENT = "parent"
    RELATIVE = "relative"
    COLLEAGUE = "colleague"
    OTHER = "other"

    @classmethod
    def choices(cls):
        return [(r.value, r.name.replace("_", " ").title()) for r in cls]
