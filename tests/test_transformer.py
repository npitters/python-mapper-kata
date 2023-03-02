import pytest
import json
from app.transformer import transform


def test_transform_with_source_id_returns_id():
    data = {
        "id": 101,
        "name": "Jumper Smith",
        "class": "Junior",
        "eventClassification": "B",
        "eventTypeId": 2,
        "eventId": 2003,
        "marks": "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in",
    }

    result = transform(data)

    assert result["id"] == 101


def test_transform_with_invalid_source_id_field_returns_exception_with_missing_field_id():
    data = {"id": ""}

    with pytest.raises(Exception) as err:
        transform(data)

    assert "Missing required field, 'id'" in str(err.value)


def test_transform_with_missing_source_id_field_returns_exception():
    data = {}

    with pytest.raises(Exception) as err:
        transform(data)

    assert "Missing required field, ''" in str(err.value)


def test_transform_with_valid_source_name_field_maps_lastname_firstname():
    data = {"id": 123, "name": "Usain Bolt", "class": "Junior", "eventClassification": "B", "eventId": 2003}

    actual_result = transform(data)

    assert actual_result["firstName"] == "Usain"
    assert actual_result["lastName"] == "Bolt"


def test_transform_with_valid_source_name_field_maps_lastname_only_with_no_firstname():
    data = {"id": 123, "name": "Bolt", "class": "Junior", "eventClassification": "B", "eventId": 2006}

    actual_result = transform(data)

    assert "firstName" not in actual_result
    assert actual_result["lastName"] == "Bolt"


def test_transform_with_valid_source_name_field_maps_lastname_as_unknown_when_missing():
    data = {"id": 123, "name": "", "class": "Junior", "eventClassification": "B", "eventId": 1006}

    actual_result = transform(data)

    assert actual_result["lastName"] == "Unknown"


def test_transform_with_missing_source_school_name_field_maps_default_name():
    data = {"id": 123, "name": "Usain Bolt", "class": "Junior", "eventClassification": "B", "eventId": 2005}

    actual_result = transform(data)

    assert actual_result["school"] == "Papillion Lavistia High School"


def test_transform_with_missing_source_state_name_field_maps_default_name():
    data = {"id": 123, "name": "Usain Bolt", "class": "Junior", "eventClassification": "B", "eventId": 1005}

    actual_result = transform(data)

    assert actual_result["state"] == "NE"


def test_transform_with_valid_source_class_name_field_junior_maps_grade_as_int():
    data = {"id": 123, "name": "Usain Bolt", "class": "Junior", "eventClassification": "B", "eventId": 2006}

    actual_result = transform(data)

    assert actual_result["grade"] == 11


def test_transform_with_valid_source_class_name_field_sophomore_maps_grade_as_int():
    data = {"id": 123, "name": "Usain Bolt", "class": "Sophomore", "eventClassification": "B", "eventId": 2006}

    actual_result = transform(data)

    assert actual_result["grade"] == 10


def test_transform_with_valid_source_class_field_name_freshman_maps_grade_as_int():
    data = {"id": 123, "name": "Usain Bolt", "class": "Freshman", "eventClassification": "B", "eventId": 2001}

    actual_result = transform(data)

    assert actual_result["grade"] == 9


def test_transform_with_valid_source_class_name_field_senior_maps_grade_as_int():
    data = {"id": 123, "name": "Usain Bolt", "class": "Senior", "eventClassification": "B", "eventId": 1004}

    actual_result = transform(data)

    assert actual_result["grade"] == 12


def test_transform_with_missing_source_classification_field_returns_exception_with_missing_field_eventClassification():
    data = {"id": 123, "name": "Usain Bolt", "class": "Senior", "eventClassification": ""}

    with pytest.raises(Exception) as err:
        transform(data)

    assert "Missing required field, 'eventClassification'" in str(err.value)


def test_transform_with_valid_source_classification_field_maps_target_value_for_boys():
    data = {"id": 123, "name": "Usain Bolt", "class": "Senior", "eventClassification": "B", "eventId": 1003}

    actual_result = transform(data)

    assert actual_result["classification"] == "Boys"


def test_transform_with_valid_source_classification_field_maps_target_value_for_girls():
    data = {"id": 123, "name": "Lilliane Bolt", "class": "Senior", "eventClassification": "G", "eventId": 1003}

    actual_result = transform(data)

    assert actual_result["classification"] == "Girls"


def test_transform_with_valid_source_event_name_field_maps_target_value_for_eventid_name_pole_vault():
    data = {"id": 123, "name": "Lilliane Bolt", "class": "Senior", "eventClassification": "G", "eventId": 2003}

    actual_result = transform(data)

    assert actual_result["eventName"] == "Pole Vault"

