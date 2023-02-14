class MissingRequiredFieldException(Exception):
    pass


def transform(raw_data):
    transform_data = {}
    if not raw_data:
        raise MissingRequiredFieldException("Missing required field")
    if not raw_data["id"]:
        raise MissingRequiredFieldException("Missing required field")
    name = _parse_name(raw_data["name"])
    if len(name) > 1:
        transform_data["firstName"] = _name_transformer(name, 1)[0]
        transform_data["lastName"] = _name_transformer(name, 1)[1]
    else:
        transform_data["lastName"] = _name_transformer(name)
    transform_data["id"] = raw_data["id"] 
    return transform_data

def _parse_name(data):
    return data.split(" ")

def _name_transformer(name, index=0):
    if index > 0:
        firstName = name[0]
        lastName = name[1]
        return (firstName, lastName)
    lastName = "Unknown" if not name[0] else name[0]
    return lastName
