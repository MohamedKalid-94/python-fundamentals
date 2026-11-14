from pydantic import (BaseModel, ConfigDict, Field, ValidationError,
                      field_validator, model_validator)

# PYDANTIC checks and converts data using type hints. FastAPI is built on it.
# This lesson uses Pydantic ALONE, so you see exactly what FastAPI does for a request body.
# Install: it comes with FastAPI.  This course uses Pydantic v2.
#
# A MODEL is a class that inherits BaseModel. Creating an object VALIDATES the input:
#   right type                 kept
#   convertible (lax mode)     "5" becomes 5, "21.5" becomes 21.5
#   wrong                      ValidationError (with ALL the problems, not just the first)
#
# PYDANTIC v1 -> v2 NAMES (old tutorials use the left column)
#   .dict()            .model_dump()           .json()            .model_dump_json()
#   .parse_obj(d)      .model_validate(d)      .parse_raw(s)      .model_validate_json(s)
#   @validator         @field_validator        @root_validator    @model_validator
#   class Config:      model_config = ConfigDict(...)             .schema()   .model_json_schema()
#   orm_mode = True    from_attributes = True


class Sensor(BaseModel):
    id: int
    name: str
    unit: str = "C"                 # a default makes the field optional
    reading: float | None = None    # may be None, and defaults to None


class Reading(BaseModel):
    value: float = Field(ge=-50, le=150)            # constraints, like Query(...) in lesson 07
    label: str = Field(min_length=1, max_length=10)
    count: int = Field(default=0, ge=0)


class User(BaseModel):
    name: str
    age: int

    @field_validator("name")                        # a rule for one field
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name must not be blank")
        return value.title()                        # the returned value REPLACES the input


class Range(BaseModel):
    low: int
    high: int

    @model_validator(mode="after")                  # a rule across several fields
    def check_order(self):
        if self.low > self.high:
            raise ValueError("low must be <= high")
        return self


class Message(BaseModel):
    sender_id: int = Field(alias="senderId")        # the JSON name differs from the Python name


class Frozen(BaseModel):
    model_config = ConfigDict(frozen=True)          # immutable and hashable (Module 20, file 11)
    name: str


class NoExtras(BaseModel):
    model_config = ConfigDict(extra="forbid")       # unknown keys are an error (the default is to ignore them)
    a: int


class Strict(BaseModel):
    model_config = ConfigDict(strict=True)          # no conversion: "5" is NOT accepted for an int
    n: int


# WHAT YOU GET
#   Sensor(id="5", name="t")              id == 5
#   Sensor(id="x", name=5)                ValidationError with 2 errors: int_parsing and string_type
#   Sensor(...).model_dump()              {'id': 1, 'name': 't', 'unit': 'C', 'reading': None}
#   Sensor(...).model_dump_json()         '{"id":1,"name":"t","unit":"C","reading":null}'
#   Sensor.model_json_schema()            the JSON Schema that FastAPI puts into /openapi.json
# Notes: str is NOT converted from int (5 is not "5"). Extra keys are ignored by default.
# Mutable defaults such as tags: list[str] = [] are safe: each object gets its own copy.