from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException

# TWO WAYS TO SPLIT A BIG API
#
# 1. APIRouter: one APPLICATION, many FILES. Routes are grouped and included with a prefix.
#      - the routers share one /docs, one OpenAPI document, one set of middleware
#      - prefix, tags and dependencies can be set once per router (or per include_router)
#      - this is the normal way to organise a project
#
# 2. app.mount("/v1", sub_app): a COMPLETE, independent application under a path.
#      - its own /docs and /openapi.json (at /v1/docs), its own middleware and exception handlers
#      - NOT listed in the main application's documentation
#      - good for API versions, or to hold another ASGI/WSGI app (lesson 09)
#
# SUGGESTED PROJECT LAYOUT
#   app/
#     main.py          create FastAPI(lifespan=...), add middleware, include the routers
#     config.py        Settings (pydantic-settings)
#     deps.py          shared dependencies: database session, current user
#     routers/         users.py  items.py  ...   (one APIRouter each)
#     schemas/         Pydantic models (input and output)
#     models/          database tables
#     services/        business logic with no FastAPI imports: easy to test
#   tests/             mirror the layout, use TestClient and dependency_overrides


def require_admin(x_role: Annotated[str | None, Header()] = None):
    if x_role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")


users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("")
def list_users():
    return [{"id": 1, "name": "ann"}, {"id": 2, "name": "bo"}]


@users_router.get("/{user_id}")
def read_user(user_id: int):
    return {"id": user_id, "name": "ann"}


# A dependency on the whole router: every route in it is protected
admin_router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


@admin_router.get("/stats")
def stats():
    return {"users": 2}


# Routers can be nested: /api/users and /api/admin/stats
api = APIRouter(prefix="/api")
api.include_router(users_router)
api.include_router(admin_router)

app = FastAPI(title="Main app")
app.include_router(api)

# Mounted sub-applications: two versions of an API
v1 = FastAPI(title="API v1")


@v1.get("/status")
def v1_status():
    return {"version": 1}


v2 = FastAPI(title="API v2")


@v2.get("/status")
def v2_status():
    return {"version": 2}


app.mount("/v1", v1)
app.mount("/v2", v2)