import pytest
import json
from app.transformer import transform, MissingRequiredValueException

def test_transform_with_valid_id_field_returns():
    with open("tests/test_data/valid_ntfd_data.json", encoding="utf-8") as f:
        data = json.load(f)

    result = transform(data)

    assert result is not None

def test_transform_with_invalid_id_field_returns_exception():
    with open("tests/test_data/invalid_id_field.json", encoding="utf-8") as f:
        data = json.load(f)

    with pytest.raises(MissingRequiredValueException) as err:
        transform(data)
        assert "Missing or invalid required field 'id'" in str(err.value)

def test_transform_with_missing_id_field_returns_exception():
    with open("tests/test_data/missing_id_field.json", encoding="utf-8") as f:
        data = json.load(f)

    with pytest.raises(MissingRequiredValueException) as err:
        transform(data)
        assert "Missing or required field 'id'" in str(err.value)
