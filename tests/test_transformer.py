import pytest
import json
from app.transformer import transform



def test_transform_with_valid_id_maps_id():
    data = {
        "id": 101,
        "name": "Jumper Smith",
        "class": "Junior",
        "eventClassification": "B",
        "eventTypeId": 2,
        "eventId": 2003,
        "marks": "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in"
    }

    result = transform(data)

    assert result["id"] == 101

def test_transform_with_invalid_id_field_returns_exception():
    data = {"id": None}

    with pytest.raises(Exception) as err:
        transform(data)

    assert err.value.args[0] == "Missing required field"

def test_transform_with_missing_id_field_returns_exception():
    data = {}

    with pytest.raises (Exception) as err:
        transform(data)

    assert err.value.args[0] == "Missing required field"

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