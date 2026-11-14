from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, Field

# CRUD = Create, Read, Update, Delete: the four things you do with a stored resource.
#   CREATE   POST   /sensors            body = SensorCreate      -> 201 + the new record
#   READ     GET    /sensors            list (paging, filter)    -> 200
#            GET    /sensors/{id}       one                      -> 200 or 404
#   UPDATE   PUT    /sensors/{id}       REPLACE the whole record -> 200 (missing fields get their defaults)
#            PATCH  /sensors/{id}       change ONLY the sent fields -> 200
#   DELETE   DELETE /sensors/{id}                                -> 204, no body
#
# GOOD HABITS
#   - separate models: Create (input), Update (all optional), Read (output, adds the id)
#   - PATCH: model_dump(exclude_unset=True) gives only the fields the client sent
#   - 404 for a missing id, 409 Conflict for a duplicate, 422 (automatic) for bad data
#   - paging: skip and limit, with a maximum limit
# This lesson keeps the data in a dict. Lesson 02 puts the SAME API on a real database.

app = FastAPI()


class SensorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=30)
    unit: str = "C"
    location: str | None = None


class SensorUpdate(BaseModel):                  # for PATCH: everything is optional
    name: str | None = Field(default=None, min_length=1, max_length=30)
    unit: str | None = None
    location: str | None = None


class SensorRead(SensorCreate):
    id: int


db: dict[int, dict] = {}
next_id = 1


def reset():
    global next_id
    db.clear()
    next_id = 1


def find_or_404(sensor_id: int) -> dict:
    if sensor_id not in db:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return db[sensor_id]


def name_taken(name: str, except_id: int | None = None) -> bool:
    return any(s["name"] == name and s["id"] != except_id for s in db.values())


@app.post("/sensors", response_model=SensorRead, status_code=201)
def create_sensor(sensor: SensorCreate):
    global next_id
    if name_taken(sensor.name):
        raise HTTPException(status_code=409, detail="A sensor with this name already exists")
    record = {"id": next_id, **sensor.model_dump()}
    db[next_id] = record
    next_id += 1
    return record


@app.get("/sensors", response_model=list[SensorRead])
def list_sensors(
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
    unit: str | None = None,
):
    sensors = [s for s in db.values() if unit is None or s["unit"] == unit]
    return sensors[skip: skip + limit]


@app.get("/sensors/{sensor_id}", response_model=SensorRead)
def read_sensor(sensor_id: int):
    return find_or_404(sensor_id)


@app.put("/sensors/{sensor_id}", response_model=SensorRead)
def replace_sensor(sensor_id: int, sensor: SensorCreate):
    find_or_404(sensor_id)
    if name_taken(sensor.name, except_id=sensor_id):
        raise HTTPException(status_code=409, detail="A sensor with this name already exists")
    db[sensor_id] = {"id": sensor_id, **sensor.model_dump()}
    return db[sensor_id]


@app.patch("/sensors/{sensor_id}", response_model=SensorRead)
def change_sensor(sensor_id: int, update: SensorUpdate):
    stored = find_or_404(sensor_id)
    # exclude_unset: only what the client sent. exclude_none: a "null" cannot blank a field.
    changes = update.model_dump(exclude_unset=True, exclude_none=True)
    if "name" in changes and name_taken(changes["name"], except_id=sensor_id):
        raise HTTPException(status_code=409, detail="A sensor with this name already exists")
    stored.update(changes)
    return stored


@app.delete("/sensors/{sensor_id}", status_code=204)
def delete_sensor(sensor_id: int):
    find_or_404(sensor_id)
    del db[sensor_id]
    return Response(status_code=204)