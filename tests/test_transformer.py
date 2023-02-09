from app.transformer import transform


def test_transform_returns_something():
    result = transform({"id": 1})

    assert result is not None
