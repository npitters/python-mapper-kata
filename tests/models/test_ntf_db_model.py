import json
from app.models.ntf_db_model import TrackAndFieldDb


def test_from_json_with_valid_schema():
    data = {
        "id": 101,
        "name": "Jumper Smith",
        "class": "Junior",
        "eventClassification": "B",
        "eventTypeId": 2,
        "eventId": 2003,
        "marks": "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in",
    }

    result = TrackAndFieldDb.from_json(data)

    assert result.id == "101"
    assert result.name == "Jumper Smith"
    assert result.grade == "Junior"
    assert result.classification == "B"
