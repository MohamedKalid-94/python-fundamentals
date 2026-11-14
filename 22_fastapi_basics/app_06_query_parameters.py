from fastapi import FastAPI

# QUERY PARAMETERS are the ?key=value&key=value part of the URL.
# Any function parameter that is NOT in the path becomes a query parameter.
#   has a default value   -> optional           (skip: int = 0)
#   default None          -> optional, may be absent  (q: str | None = None)
#   no default            -> REQUIRED          (q: str)  missing -> 422
# Booleans accept: true/false, 1/0, yes/no, on/off.

app = FastAPI()

fake_items = [{"name": name} for name in ("pen", "ink", "cap", "ruler", "tape")]


# 1. Pagination: the classic use
@app.get("/items")
def list_items(skip: int = 0, limit: int = 10):
    return fake_items[skip: skip + limit]


# 2. A required query parameter and a boolean flag
@app.get("/search")
def search(q: str, exact: bool = False):
    names = [item["name"] for item in fake_items]
    found = [n for n in names if (n == q if exact else q in n)]
    return {"query": q, "exact": exact, "found": found}


# 3. Path and query parameters together (FastAPI tells them apart by the path template)
@app.get("/users/{user_id}/orders")
def user_orders(user_id: int, status: str | None = None, page: int = 1):
    return {"user_id": user_id, "status": status, "page": page}


# URLs:  /items?skip=1&limit=2      /search?q=p       /search?q=pen&exact=true
#        /users/7/orders?status=open&page=2
# In PowerShell put the URL in quotes: the & character has a meaning there.