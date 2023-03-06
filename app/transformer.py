from enum import Enum


EVENT_NAMES = {
    1001: "100m",
    1002: "200m",
    1003: "400m",
    1004: "800m",
    1005: "1600m",
    1006: "3200m",
    2001: "Long Jump",
    2002: "Triple Jump",
    2003: "Pole Vault",
    2004: "High Jump",
    2005: "Shot Put",
    2006: "Discus",
}


EVENT_TYPE = {
    1: "times",
    2: "marks"
}


class ClassificationKey(Enum):
    G = "Girls"
    B = "Boys"


class GradeMapping(Enum):
    def __str__(self):
        return "%s" % self.value

    Freshman = 9
    Sophomore = 10
    Junior = 11
    Senior = 12


class MissingRequiredFieldException(Exception):
    def __init__(self, field=None):
        self.field = field

        default_message = f"Missing required field, '{field}'"
        super().__init__(default_message)


DEFAULT_SCHOOL_NAME = "Papillion Lavistia High School"
DEFAULT_STATE_NAME = "NE"


def transform(raw_data):
    transform_data = {}

    if not raw_data:
        raise MissingRequiredFieldException("Missing required field, ''")
    if not raw_data["id"]:
        raise MissingRequiredFieldException("Missing required field, 'id'")
    if not raw_data["class"]:
        raise MissingRequiredFieldException("Missing required field, 'class'")
    if not raw_data["eventClassification"]:
        raise MissingRequiredFieldException(
            "Missing required field, 'eventClassification'"
        )

    name = _parse_name(raw_data["name"])

    if len(name) > 1:
        transform_data["firstName"] = _name_transformer(name, 1)[0]
        transform_data["lastName"] = _name_transformer(name, 1)[1]
    else:
        transform_data["lastName"] = _name_transformer(name)

    transform_data["id"] = str(_id_transformer(raw_data))
    transform_data["school"] = DEFAULT_SCHOOL_NAME
    transform_data["state"] = DEFAULT_STATE_NAME
    transform_data["grade"] = _grade_transformer(raw_data["class"])
    transform_data["classification"] = _classification_transformer(
        raw_data["eventClassification"]
    )
    transform_data["eventName"] = _event_name_transformer(raw_data["eventId"])
    if raw_data["eventTypeId"]:
        transform_data["personalBest"] = _event_type_id_transformer(raw_data["eventTypeId"])

    return transform_data


def _id_transformer(id_name):
    return id_name["id"]


def _parse_name(full_name):
    return full_name.split(" ")


def _grade_transformer(class_data):
    return GradeMapping[class_data].value


def _name_transformer(full_name, index=0):
    if index > 0:
        firstName = full_name[0]
        lastName = full_name[1]
        return (firstName, lastName)
    lastName = "Unknown" if not full_name[0] else full_name[0]

    return lastName


def _classification_transformer(class_name):
    return ClassificationKey[class_name].value


def _event_name_transformer(event_id):
    return EVENT_NAMES[event_id]

def _event_type_id_transformer(event_type_id):
    int(event_type_id)
    return EVENT_TYPE[event_type_id]
