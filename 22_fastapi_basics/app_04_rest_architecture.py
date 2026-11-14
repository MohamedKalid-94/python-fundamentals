from fastapi import FastAPI, HTTPException, Response, status

# REST: a style for designing APIs on top of HTTP.
#   RESOURCES    things with a name, written as NOUNS in the URL:  /items   /items/3   /users/7/orders
#   METHODS      the verb says what to do with the resource
#   STATELESS    every request carries everything the server needs; no hidden session
#   REPRESENTATION  the data travels as JSON (also XML, CSV ...)
#   STATUS CODES the result is in the code, not only in the text
#
#   METHOD   MEANING                    SAFE   IDEMPOTENT   TYPICAL SUCCESS CODE
#   GET      read                       yes    yes          200
#   POST     create (or run an action)  no     no           201 Created
#   PUT      replace the whole thing    no     yes          200
#   PATCH    change part of it          no     no           200
#   DELETE   remove                     no     yes          204 No Content
#   (safe = changes nothing, idempotent = doing it twice leaves the same state as once)
#
#   CODE   MEANING                          CODE   MEANING
#   200    OK                               404    Not Found
#   201    Created                          409    Conflict
#   204    No Content                       422    Validation error (FastAPI's choice)
#   400    Bad Request                      500    Internal Server Error
#   401    Unauthorized (not logged in)     503    Service Unavailable
#   403    Forbidden (not allowed)
#
# URL DESIGN:  /items (the collection)   /items/3 (one member).  Plural nouns, no verbs: not /getItem.
# Query parameters (next lessons) filter, sort and page:  /items?limit=10&skip=20
#
# This lesson keeps data in memory and takes the name from the QUERY string. Lesson 09
# replaces that with a JSON body, which is the normal way for POST and PUT.

app = FastAPI()

items: dict[int, str] = {}
next_id = 3


def reset():
    global next_id
    items.clear()
    items.update({1: "pen", 2: "ink"})
    next_id = 3


reset()


@app.get("/items")
def list_items():
    return [{"id": item_id, "name": name} for item_id, name in items.items()]


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"id": item_id, "name": items[item_id]}


@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(name: str):
    global next_id
    item_id = next_id
    next_id += 1
    items[item_id] = name
    return {"id": item_id, "name": name}


@app.put("/items/{item_id}")
def replace_item(item_id: int, name: str):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    items[item_id] = name
    return {"id": item_id, "name": name}


@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del items[item_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)     # 204 has no body