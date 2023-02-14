from enum import Enum

class GradeMapping(Enum):
    def __str__(self):
        return '%s' % self.value
    Freshman = 9
    Sophomore = 10
    Junior = 11
    Senior = 12
class MissingRequiredFieldException(Exception):
    pass

DEFAULT_SCHOOL_NAME = "Papillion Lavistia High School"
DEFAULT_STATE_NAME = "NE"

def transform(raw_data):
    transform_data = {}

    if not raw_data:
        raise MissingRequiredFieldException("Missing required field")
    if not raw_data["id"]:
        raise MissingRequiredFieldException("Missing required field")
    if not raw_data["class"]:
        raise MissingRequiredFieldException("Missing required field")
    name = _parse_name(raw_data["name"])

    if len(name) > 1:
        transform_data["firstName"] = _name_transformer(name, 1)[0]
        transform_data["lastName"] = _name_transformer(name, 1)[1]
    else:
        transform_data["lastName"] = _name_transformer(name)
    transform_data["id"] = raw_data["id"]
    transform_data["school"] = DEFAULT_SCHOOL_NAME
    transform_data["state"] = DEFAULT_STATE_NAME
    transform_data["grade"] = _grade_transformer(raw_data["class"])
    return transform_data

def _parse_name(data):
    return data.split(" ")

def _grade_transformer(class_name):
    return GradeMapping[class_name].value

def _name_transformer(name, index=0):
    if index > 0:
        firstName = name[0]
        lastName = name[1]
        return (firstName, lastName)
    lastName = "Unknown" if not name[0] else name[0]

    return lastName
