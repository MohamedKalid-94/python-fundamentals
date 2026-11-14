from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

# A REQUEST BODY is the data a client SENDS (JSON), normally with POST, PUT or PATCH.
# Declare a parameter whose type is a Pydantic model and FastAPI will:
#   1. read the body as JSON            2. validate and convert it with the model
#   3. give you a model object          4. describe it in /docs (with an example you can edit and send)
#
# HOW FASTAPI DECIDES where a parameter comes from:
#   name appears in the path          -> path parameter
#   a simple type (int, str, bool...) -> query parameter
#   a Pydantic model                  -> request body
# Send a body with: Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/items `
#                      -ContentType "application/json" -Body '{"name":"pen","price":10}'

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float = Field(gt=0)
    tags: list[str] = []
    description: str | None = None


class User(BaseModel):
    username: str


# 1. One model as the body
@app.post("/items", status_code=201)
def create_item(item: Item):
    data = item.model_dump()
    data["price_with_tax"] = round(item.price * 1.18, 2)
    return data


# 2. Path + query + body in one function
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, notify: bool = False):
    return {"item_id": item_id, "notify": notify, **item.model_dump()}


# 3. TWO models: the JSON must contain one key per parameter name
#    {"item": {...}, "user": {...}}
@app.post("/orders")
def create_order(item: Item, user: User):
    return {"item": item.name, "user": user.username}


# 4. A single plain value as the body: the JSON is just the value:  3
@app.post("/importance")
def set_importance(importance: Annotated[int, Body(ge=1, le=5)]):
    return {"importance": importance}


# 5. The same, but wrapped in a key (embed=True):  {"score": 4}
@app.post("/rating")
def rating(score: Annotated[int, Body(embed=True, ge=1, le=5)]):
    return {"score": score}


# NOTES
#  - A bad body gives 422 with "loc" starting with "body":  ["body", "price"]
#  - Extra keys in the JSON are ignored.
#  - GET requests should not have a body.
#  - Nested models, lists of models and response models come in Module 23.