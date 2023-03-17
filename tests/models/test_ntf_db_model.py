import json
from app.models.ntf_db_model import TrackAndFieldDb


def test_from_json_with_valid_schema_and_score_as_marks():
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
    assert result.event_name == 2003
    assert result.personal_best == 2
    assert result.personal_score == "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in"


def test_from_json_with_valid_schema_and_score_as_times():
    data = {
        "id": 100,
        "name": "Runner Jones",
        "class": "Senior",
        "eventClassification": "G",
        "eventTypeId": 1,
        "eventId": 1001,
        "times": "13.50|13.81|12.74|13.44|13.71"
    }

    result = TrackAndFieldDb.from_json(data)

    assert result.id == "100"
    assert result.name == "Runner Jones"
    assert result.grade == "Senior"
    assert result.classification == "G"
    assert result.event_name == 1001
    assert result.personal_best == 1
    assert result.personal_score == "13.50|13.81|12.74|13.44|13.71"