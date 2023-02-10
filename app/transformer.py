class MissingRequiredFieldException(Exception):
    pass


def transform(raw_data):
    payload_data = {}
    if not raw_data:
        raise MissingRequiredFieldException("Missing required field")
    if not raw_data["id"]:
        raise MissingRequiredFieldException("Missing required field")
    if raw_data["name"]:
        name = _parse_name(raw_data["name"])
        if name and len(name) > 1:
            firstName = name[0]
            lastName = name[1]
            payload_data["firstName"] = firstName
            payload_data["lastName"] = lastName
        else:
            lastName = name[0]
            payload_data["lastName"] = lastName
    payload_data["id"] = raw_data["id"] 
    return payload_data

def _parse_name(data):
    return data.split(" ")
