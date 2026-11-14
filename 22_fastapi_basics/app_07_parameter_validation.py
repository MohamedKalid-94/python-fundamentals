from typing import Annotated

from fastapi import FastAPI, Path, Query

# Add rules to a parameter with Query(...) and Path(...) inside Annotated[...].
# Annotated[TYPE, Query(rules)] is the current recommended style: the default value stays a plain default.
#
#   numbers   gt (>)   ge (>=)   lt (<)   le (<=)
#   text      min_length   max_length   pattern (a regular expression, Module 17)
#   docs      title   description   deprecated=True   include_in_schema=False
#   other     alias="item-query"   (the name in the URL differs from the Python name)
#   lists     Annotated[list[str] | None, Query()]   for ?tag=a&tag=b
# ("pattern" replaced the old name "regex".)
# A failed rule gives 422 and the function is NOT called.

app = FastAPI()


@app.get("/items/{item_id}")
def read_item(
    item_id: Annotated[int, Path(title="Item id", ge=1, le=1000)],
    q: Annotated[str | None, Query(min_length=3, max_length=20)] = None,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return {"item_id": item_id, "q": q, "size": size}


@app.get("/codes")
def codes(code: Annotated[str, Query(pattern=r"^[A-Z]{3}-\d{3}$")]):
    return {"code": code}


@app.get("/multi")
def multi(tag: Annotated[list[str] | None, Query()] = None):
    return {"tags": tag or []}


@app.get("/aliased")
def aliased(item_query: Annotated[str, Query(alias="item-query")] = "none"):
    return {"item_query": item_query}


# Error types you will see in the "type" field:
#   greater_than  greater_than_equal  less_than  less_than_equal
#   string_too_short  string_too_long  string_pattern_mismatch  missing  int_parsing