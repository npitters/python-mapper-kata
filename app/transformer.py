from app.models.national_track_and_field_database import TrackData


class MissingRequiredValueException(Exception):
    pass


def transform(raw_data: TrackData):
    if not raw_data:
        raise MissingRequiredValueException("Missing or required field 'id'")
    if not raw_data["id"]:
        raise MissingRequiredValueException("Missing or required field 'id'")
    return raw_data
