from enum import Enum

from fastapi import FastAPI

# A PATH PARAMETER is a variable part of the URL, written in { } and received as a function argument.
# The type hint converts and validates it:  /users/5  ->  user_id == 5 (an int, not "5").

app = FastAPI()


# ORDER MATTERS: FastAPI checks paths from the top. A FIXED path must come BEFORE a variable one,
# or /users/me would be taken as user_id="me" (and fail with 422).
@app.get("/users/me")
def read_me():
    return {"user": "the current user"}


@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}


# A path that may contain slashes: ":path" converter
@app.get("/files/{file_path:path}")
def read_file(file_path: str):
    return {"file_path": file_path}


# Only some values allowed: an Enum (a str subclass, so JSON shows the value)
class Sensor(str, Enum):
    temperature = "temperature"
    humidity = "humidity"


@app.get("/sensors/{kind}")
def read_sensor(kind: Sensor):
    if kind is Sensor.temperature:
        return {"kind": kind.value, "unit": "C"}
    return {"kind": kind.value, "unit": "%"}


# /docs shows the allowed values of "kind" as a drop-down list.
# Other types work too: float, bool, UUID, datetime, date ...
# Constraints (ge, le, pattern ...) come in lesson 07.