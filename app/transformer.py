class MissingRequiredFieldException(Exception):
    pass


def transform(raw_data):
    if not raw_data:
        raise MissingRequiredFieldException("Missing required field")
    if not raw_data["id"]:
        raise MissingRequiredFieldException("Missing required field")
    return raw_data
