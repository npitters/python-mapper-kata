from enum import Enum


DEFAULT_SCHOOL_NAME = "Papillion Lavistia High School"
DEFAULT_STATE_NAME = "NE"
DEFAULT_MESSAGE = "Missing required field"

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

        default_message = f"{DEFAULT_MESSAGE}, '{field}'"
        super().__init__(default_message)


def transform(request_data):
    response_dict = {}

    if not request_data["id"]:
        raise MissingRequiredFieldException(f"{DEFAULT_MESSAGE}, 'id'")
    if not request_data["class"]:
        raise MissingRequiredFieldException(f"{DEFAULT_MESSAGE}, 'class'")
    if not request_data["eventClassification"]:
        raise MissingRequiredFieldException(
            f"{DEFAULT_MESSAGE}, 'eventClassification'"
        )

    name = _parse_name(request_data["name"])

    if len(name) > 1:
        response_dict["firstName"] = _name_transformer(name, 1)[0]
        response_dict["lastName"] = _name_transformer(name, 1)[1]
    else:
        response_dict["lastName"] = _name_transformer(name)

    response_dict["id"] = str(_id_transformer(request_data))
    response_dict["school"] = DEFAULT_SCHOOL_NAME
    response_dict["state"] = DEFAULT_STATE_NAME
    response_dict["grade"] = _grade_transformer(request_data["class"])
    response_dict["classification"] = _classification_transformer(
        request_data["eventClassification"]
    )
    response_dict["eventName"] = _event_name_transformer(request_data["eventId"])
    if request_data["eventTypeId"]:
        score_key = _event_type_id_transformer(request_data["eventTypeId"])
        score_data = request_data[score_key]
        response_dict["personalBest"] = _find_personal_best_score(score_data, score_key)

    return response_dict


def _id_transformer(id_name):
    return id_name["id"]


def _parse_name(full_name):
    return full_name.split(" ")


def _grade_transformer(class_data):
    return GradeMapping[class_data].value


def _name_transformer(full_name, index=0):
    if index > 0:
        first_name = full_name[0]
        last_name = full_name[1]
        return (first_name, last_name)
    last_name = "Unknown" if not full_name[0] else full_name[0]

    return last_name


def _classification_transformer(class_name):
    return ClassificationKey[class_name].value


def _event_name_transformer(event_id):
    return EVENT_NAMES[event_id]


def _event_type_id_transformer(event_type_id):
    int(event_type_id)
    return EVENT_TYPE[event_type_id]


def _find_personal_best_score(score_data, score_key):
    scores_list = score_data.split("|")
    if score_key == "times":
        lowest_score = sorted(scores_list, reverse=True)[0]
        return lowest_score
    else:
        highest_score = _sort_high_score(scores_list)
        return highest_score


def _sort_high_score(scores_list):
    scores_list.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
    return scores_list[-1]
     
