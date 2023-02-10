import pytest
import json
from app.transformer import transform, MissingRequiredFieldException


def test_transform_with_valid_id_field():
    with open("tests/models/test_data/valid_fields.json", encoding="utf-8") as f:
        data = json.load(f)

    result = transform(data)

    assert result is not None

def test_transform_with_invalid_id_field_returns_exception():
    with open("tests/models/test_data/invalid_fields.json", encoding="utf-8") as f:
        data = json.load(f)

    with pytest.raises(MissingRequiredFieldException) as err:
        transform(data)
    assert "Missing required field" in str(err.value)

def test_transform_with_missing_id_field_returns_exception():
    with open("tests/models/test_data/missing_fields.json", encoding="utf-8") as f:
        data = json.load(f)

    with pytest.raises(MissingRequiredFieldException) as err:
        transform(data)
    assert "Missing required field" in str(err.value)

def test_transform_with_valid_name_maps_lastname_firstname():
    data = {
        "id": 123,
        "name": "Joe Biden"
    }

    actual_result = transform(data)

    assert actual_result["firstName"] == "Joe"
    assert actual_result['lastName'] == "Biden"

def test_transform_with_valid_name_maps_lastname_only_with_no_firstname():
    data = {
        "id": 123,
        "name": "Biden"
    }

    actual_result = transform(data)

    assert "firstName" not in actual_result
    assert actual_result['lastName'] == "Biden"