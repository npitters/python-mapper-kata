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
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(100, "Usain Bolt", "Junior", "B", 2003, 2)],
)
def test_transform_with_source_athlete_name_field_maps_target_lastname_firstname(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "Usain" == actual_result["firstName"]
    assert "Bolt" == actual_result["lastName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Bolt", "Junior", "B", 2006, 2)],
)
def test_transform_with_source_athlete_name_missing_firstname_maps_target_lastname_only_with_no_firstname(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "firstName" not in actual_result
    assert expected_data["name"] == actual_result["lastName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "", "Junior", "B", 2006, 1)],
)
def test_transform_with_source_athlete_name_field_missing_maps_target_lastname_as_unknown_when_missing(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "Unknown" == actual_result["lastName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Michael Bolt", "Junior", "B", 2005, 1)],
)
def test_transform_with_source_athlete_school_name_field_maps_target_default_school_name(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "Papillion Lavistia High School" == actual_result["school"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Usain Bolt", "Junior", "B", 1005, 1)],
)
def test_transform_with_source_athlete_state_name_field_maps_default_state_name(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "NE" == actual_result["state"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Asafa Powell", "Junior", "B", 2006, 2)],
)
def test_transform_with_source_athlete_class_name_field_junior_maps_grade_as_int_11(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert 11 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Yohan Blake", "Sophomore", "B", 2006, 1)],
)
def test_transform_with_source_athlete_class_name_field_sophomore_maps_grade_as_int_10(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert 10 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Usain Bolt", "Freshman", "B", 2001, 1)],
)
def test_transform_with_source_athlete_class_field_name_freshman_maps_grade_as_int_9(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert 9 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Usain Bolt", "Senior", "B", 1004, 2)],
)
def test_transform_with_source_athlete_class_name_field_senior_maps_grade_as_int_12(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert 12 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id",
    [(123, "Usain Bolt", "Senior", "", 1004)],
)
def test_transform_with_source_missing_athlete_classification_field_returns_exception_with_missing_field_event_classification(
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
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Usain Bolt", "Senior", "B", 1003, 2)],
)
def test_transform_with_source_athlete_classification_field_maps_target_value_for_boys(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "Boys" == actual_result["classification"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Lilliane Bolt", "Senior", "G", 1003, 1)],
)
def test_transform_with_source_athlete_classification_field_maps_target_value_for_girls(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "Girls" == actual_result["classification"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 1)],
)
def test_transform_with_source_id_field_2003_maps_target_value_for_event_name_as_pole_vault(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "Pole Vault" in actual_result["eventName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 2)],
)
def test_transform_with_source_field_athlete_event_type_id_2_map_the_correct_target_field_as_marks(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "marks" == actual_result["personalBest"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 1)],
)
def test_transform_with_source_field_athlete_event_type_id_1_map_the_correct_target_field_as_times(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id
    }

    actual_result = transform(expected_data)

    assert "times" == actual_result["personalBest"]