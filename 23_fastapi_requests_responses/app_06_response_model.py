import itertools

from fastapi import FastAPI
from pydantic import BaseModel

# RESPONSE MODEL: a Pydantic model that describes what you SEND BACK.
#   @app.post("/users", response_model=UserOut)       (or the return annotation:  -> UserOut)
# FastAPI then:
#   1. FILTERS the data: fields that are not in the model (a password, an internal flag) are removed
#   2. CONVERTS and VALIDATES it: a bug in your code becomes a 500 error, not wrong data for the client
#   3. DOCUMENTS the answer in /docs and openapi.json
# Never return the same model you received when it holds secrets: use separate In and Out models.
# Options:  response_model_exclude_unset=True   leave out fields that were never set (partial updates, defaults)
#           response_model_exclude_none=True    leave out None values
#           response_model_include={"a"} / response_model_exclude={"b"}   pick fields
#           response_model=list[UserOut]        a list of models

app = FastAPI()


class UserBase(BaseModel):
    username: str
    full_name: str | None = None


class UserIn(UserBase):
    password: str                   # comes IN, never goes out


class UserOut(UserBase):
    id: int


users: dict[int, dict] = {}
ids = itertools.count(1)


def reset():
    global ids
    users.clear()
    ids = itertools.count(1)


@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: UserIn):
    record = {"id": next(ids), **user.model_dump()}        # the stored record DOES hold the password
    users[record["id"]] = record
    return record                                          # ...but the response model filters it out


@app.get("/users", response_model=list[UserOut])
def list_users():
    return list(users.values())


# exclude_unset: only the fields that were really set in the returned data
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
}


@app.get("/items/{key}", response_model=Item, response_model_exclude_unset=True)
def read_item(key: str):
    return items[key]


# The response model also CHECKS your output: this returns a bad id, so FastAPI answers 500
@app.get("/broken", response_model=UserOut)
def broken():
    return {"id": "not-a-number", "username": "x"}