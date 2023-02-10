import json
from app.models.ntf_db_model import TrackAndFieldDb

def test_from_json_with_valid_schema():
    with open("tests/models/test_data/valid_fields.json", encoding="utf-8") as f:
        data = json.load(f)

    result = TrackAndFieldDb.from_json(data)

    assert result.id == "101"
    assert result.name == "Jumper Smith"
