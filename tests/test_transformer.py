import pytest
import json
from app.transformer import transform


@pytest.mark.parametrize(
    "athlete_id, expected",
    [("100", "100"), (100, "100")],
)
def test_transform_with_source_id_returns_id_string(athlete_id, expected):
    data = {
        "id": athlete_id,
        "name": "Jumper Smith",
        "class": "Junior",
        "eventClassification": "B",
        "eventTypeId": 2,
        "eventId": 2003,
        "marks": "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in",
    }

    actual_result = transform(data)

    assert expected == actual_result["id"]


@pytest.mark.parametrize("athlete_id", [("")])
def test_transform_with_invalid_source_id_field_returns_exception_with_missing_field_id(
    athlete_id,
):
    data = {"id": athlete_id}

    with pytest.raises(Exception) as err:
        transform(data)

    assert "Missing required field, 'id'" in str(err.value)


@pytest.mark.parametrize("athlete_id", [()])
def test_transform_with_missing_source_id_field_returns_exception(athlete_id):
    data = {}

    with pytest.raises(Exception) as err:
        transform(data)

    assert "Missing required field, ''" in str(err.value)


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(100, "Usain Bolt", "Junior", "B", 2003)],
)
def test_transform_with_valid_source_name_field_maps_lastname_firstname(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    test_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(test_data)

    assert actual_result["firstName"] == "Usain"
    assert actual_result["lastName"] == "Bolt"


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Bolt", "Junior", "B", 2006)],
)
def test_transform_with_valid_source_name_field_maps_lastname_only_with_no_firstname(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    test_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(test_data)

    assert "firstName" not in actual_result
    assert actual_result["lastName"] == test_data["name"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "", "Junior", "B", 2006)],
)
def test_transform_with_valid_source_name_field_maps_lastname_as_unknown_when_missing(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    test_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(test_data)

    assert actual_result["lastName"] == "Unknown"


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Michael Bolt", "Junior", "B", 2005)],
)
def test_transform_with_missing_source_school_name_field_maps_default_name(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    test_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(test_data)

    assert actual_result["school"] == "Papillion Lavistia High School"


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Usain Bolt", "Junior", "B", 1005)],
)
def test_transform_with_missing_source_state_name_field_maps_default_name(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    test_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(test_data)

    assert actual_result["state"] == "NE"


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Asafa Powell", "Junior", "B", 2006)],
)
def test_transform_with_valid_source_class_name_field_junior_maps_grade_as_int(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    test_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(test_data)

    assert actual_result["grade"] == 11


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Yohan Blake", "Sophomore", "B", 2006)],
)
def test_transform_with_valid_source_class_name_field_sophomore_maps_grade_as_int(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(expected_data)

    assert actual_result["grade"] == 10


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Usain Bolt", "Freshman", "B", 2001)],
)
def test_transform_with_valid_source_class_field_name_freshman_maps_grade_as_int(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(expected_data)

    assert actual_result["grade"] == 9


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Usain Bolt", "Senior", "B", 1004)],
)
def test_transform_with_valid_source_class_name_field_senior_maps_grade_as_int(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(expected_data)

    assert actual_result["grade"] == 12


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Usain Bolt", "Senior", "", 1004)],
)
def test_transform_with_missing_source_classification_field_returns_exception_with_missing_field_eventClassification(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
    }

    with pytest.raises(Exception) as err:
        transform(expected_data)

    assert "Missing required field, 'eventClassification'" in str(err.value)


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Usain Bolt", "Senior", "B", 1003)],
)
def test_transform_with_valid_source_classification_field_maps_target_value_for_boys(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(expected_data)

    assert actual_result["classification"] == "Boys"


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Lilliane Bolt", "Senior", "G", 1003)],
)
def test_transform_with_valid_source_classification_field_maps_target_value_for_girls(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(expected_data)

    assert actual_result["classification"] == "Girls"


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Lilliane Bolt", "Senior", "G", 2003)],
)
def test_transform_with_valid_source_event_name_field_maps_target_value_for_eventid_name_pole_vault(
    athlete_id, athlete_name, class_name, event_classification, event_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
    }

    actual_result = transform(expected_data)

    assert actual_result["eventName"] == "Pole Vault"
