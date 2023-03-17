import pytest
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


@pytest.mark.parametrize("athlete_id", [(""), ()])
def test_transform_with_invalid_source_id_field_returns_exception_with_missing_field_id(
    athlete_id,
):
    data = {"id": athlete_id}

    with pytest.raises(Exception) as err:
        transform(data)

    assert "Missing required field, 'id'" in str(err.value)


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(100, "Usain Bolt", "Junior", "B", 2003, 2, "10ft 1in|9ft 5in|14ft 0in|13ft 5in|12ft 5in")],
)
def test_transform_with_source_athlete_name_field_maps_target_lastname_firstname(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert "Usain" == actual_result["firstName"]
    assert "Bolt" == actual_result["lastName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Bolt", "Junior", "B", 2006, 2, "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in")],
)
def test_transform_with_source_athlete_name_missing_firstname_maps_target_lastname_only_with_no_firstname(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert "firstName" not in actual_result
    assert expected_data["name"] == actual_result["lastName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "", "Junior", "B", 2006, 1, "19.13|20.19|19.75|18.5")],
)
def test_transform_with_source_athlete_name_field_missing_maps_target_lastname_as_unknown_when_missing(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert "Unknown" == actual_result["lastName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Michael Bolt", "Junior", "B", 2005, 1, "20.13|20.19|19.75|18.5")],
)
def test_transform_with_source_athlete_school_name_field_maps_target_default_school_name(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert "Papillion Lavistia High School" == actual_result["school"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Usain Bolt", "Junior", "B", 1005, 1, "20.50|20.80|19.75|18.5")],
)
def test_transform_with_source_athlete_state_name_field_maps_default_state_name(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert "NE" == actual_result["state"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Asafa Powell", "Junior", "B", 2006, 2, "10ft 1in|9ft 5in|11ft 0in|13ft 5in|13ft 5in")],
)
def test_transform_with_source_athlete_class_name_field_junior_maps_grade_as_int_11(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert 11 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Yohan Blake", "Sophomore", "B", 2006, 1, "19.50|20.80|13.75|18.5")],
)
def test_transform_with_source_athlete_class_name_field_sophomore_maps_grade_as_int_10(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert 10 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Usain Bolt", "Freshman", "B", 2001, 1, "9.50|12.80|13.75")],
)
def test_transform_with_source_athlete_class_field_name_freshman_maps_grade_as_int_9(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert 9 == actual_result["grade"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Usain Bolt", "Senior", "B", 1004, 2, "10ft 1in|9ft 5in|13ft 0in|13ft 5in|14ft 5in")],
)
def test_transform_with_source_athlete_class_name_field_senior_maps_grade_as_int_12(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
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
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Usain Bolt", "Senior", "B", 1003, 2, "17ft 1in|20ft 5in|112ft 0in|13ft 7in|11ft 5in")],
)
def test_transform_with_source_athlete_classification_field_maps_target_value_for_boys(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert "Boys" == actual_result["classification"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Lilliane Bolt", "Senior", "G", 1003, 2, "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in")],
)
def test_transform_with_source_athlete_classification_field_maps_target_value_for_girls(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert "Girls" == actual_result["classification"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 2, "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in")],
)
def test_transform_with_source_id_field_2003_maps_target_value_for_event_name_as_pole_vault(
    athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert "Pole Vault" in actual_result["eventName"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 1, "13.50|14.80|12.75|9.20")],
)
def test_transform_select_lowest_time_minutes_seconds_from_list(
       athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert "9.20" == actual_result["personalBest"]



@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 1, "5:13.52|5:13.81|5:12.74|5:13.42|10:13.75")],
)
def test_transform_select_lowest_time_hours_minutes_seconds_from_list(
       athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "times": event_score
    }

    actual_result = transform(expected_data)

    assert "5:12.74" == actual_result["personalBest"]


@pytest.mark.parametrize(
    "athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score",
    [(123, "Lilliane Bolt", "Senior", "G", 2003, 2, "13ft 1in|9ft 5in|14ft 0in|13ft 5in|14ft 5in")],
)
def test_transform_select_highest_marks_from_list(
       athlete_id, athlete_name, class_name, event_classification, event_id, event_type_id, event_score
):
    expected_data = {
        "id": athlete_id,
        "name": athlete_name,
        "class": class_name,
        "eventClassification": event_classification,
        "eventId": event_id,
        "eventTypeId": event_type_id,
        "marks": event_score
    }

    actual_result = transform(expected_data)

    assert "14ft 5in" == actual_result["personalBest"]