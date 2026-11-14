import pytest
from pydantic import ValidationError

from models_08_pydantic import (Frozen, Message, NoExtras, Range, Reading, Sensor,
                                Strict, User)


def test_defaults_and_coercion():
    sensor = Sensor(id="5", name="t", reading="21.5")
    assert sensor.id == 5 and isinstance(sensor.id, int)
    assert sensor.reading == 21.5
    assert sensor.unit == "C"
    assert Sensor(id=1, name="t").reading is None


def test_validation_errors_list_every_problem():
    with pytest.raises(ValidationError) as info:
        Sensor(id="x", name=5)
    errors = info.value.errors()
    assert info.value.error_count() == 2
    assert [e["loc"] for e in errors] == [("id",), ("name",)]
    assert [e["type"] for e in errors] == ["int_parsing", "string_type"]


def test_field_constraints():
    with pytest.raises(ValidationError) as info:
        Reading(value=200, label="")
    assert {e["type"] for e in info.value.errors()} == {"less_than_equal", "string_too_short"}
    assert Reading(value=20.5, label="ok").count == 0


def test_field_validator():
    assert User(name="  ann  ", age=30).name == "Ann"
    with pytest.raises(ValidationError) as info:
        User(name="   ", age=30)
    error = info.value.errors()[0]
    assert error["type"] == "value_error"
    assert "name must not be blank" in error["msg"]


def test_model_validator():
    assert Range(low=1, high=5).high == 5
    with pytest.raises(ValidationError) as info:
        Range(low=5, high=1)
    error = info.value.errors()[0]
    assert error["loc"] == ()                       # the problem belongs to the whole model
    assert "low must be <= high" in error["msg"]


def test_alias():
    message = Message(senderId=1)
    assert message.sender_id == 1
    assert message.model_dump(by_alias=True) == {"senderId": 1}
    with pytest.raises(ValidationError):            # the Python name is NOT accepted by default
        Message(sender_id=1)


def test_frozen():
    frozen = Frozen(name="a")
    with pytest.raises(ValidationError):
        frozen.name = "b"
    assert hash(frozen) == hash(Frozen(name="a"))


def test_extra_keys():
    assert Sensor(id=1, name="t", colour="red").model_dump().get("colour") is None     # ignored
    with pytest.raises(ValidationError) as info:
        NoExtras(a=1, b=2)
    assert info.value.errors()[0]["type"] == "extra_forbidden"


def test_validate_methods():
    assert Sensor.model_validate({"id": 1, "name": "t"}).id == 1
    assert Sensor.model_validate_json('{"id": 2, "name": "h"}').name == "h"
    with pytest.raises(ValidationError) as info:
        Sensor.model_validate_json("{bad json}")
    assert info.value.errors()[0]["type"] == "json_invalid"


def test_dump_options():
    sensor = Sensor(id=1, name="t")
    assert sensor.model_dump() == {"id": 1, "name": "t", "unit": "C", "reading": None}
    assert sensor.model_dump(exclude_none=True) == {"id": 1, "name": "t", "unit": "C"}
    assert sensor.model_dump(include={"id"}) == {"id": 1}
    assert sensor.model_dump(exclude={"unit"}) == {"id": 1, "name": "t", "reading": None}
    assert sensor.model_dump_json() == '{"id":1,"name":"t","unit":"C","reading":null}'


def test_json_schema():
    schema = Sensor.model_json_schema()
    assert list(schema["properties"]) == ["id", "name", "unit", "reading"]
    assert schema["required"] == ["id", "name"]


def test_strict_mode():
    assert Strict(n=5).n == 5
    with pytest.raises(ValidationError):
        Strict(n="5")


def test_model_copy():
    original = Sensor(id=1, name="t")
    changed = original.model_copy(update={"unit": "F"})
    assert changed.unit == "F"
    assert original.unit == "C"