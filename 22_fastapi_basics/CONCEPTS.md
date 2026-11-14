# Module 22: FastAPI Basics, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Introduction | What | Web API framework: Starlette (web) + Pydantic (data), runs on ASGI, driven by type hints |
| 01 | Introduction | Gives you | Validation, conversion, automatic docs, async support, easy testing |
| 01 | Hello World | Path operation | `@app.get("/")` on a function; a returned dict becomes JSON |
| 01 | Hello World | Automatic answers | Unknown path 404, wrong method 405, bad input 422 |
| 02 | OpenAPI | Standard | JSON description of the API built from the code: `/openapi.json`, `/docs` (Swagger UI), `/redoc` |
| 02 | OpenAPI | Metadata | `FastAPI(title, description, version)`, `tags=`, `summary=`, docstring becomes description |
| 02 | OpenAPI | Switch off | `docs_url=None`, `redoc_url=None`, `openapi_url=None` |
| 02 | Uvicorn | ASGI server | `uvicorn module:app --reload` (dev), `--host`, `--port`, `--workers N` (not with reload) |
| 02 | Uvicorn | Commands | `fastapi dev file.py` (dev), `fastapi run file.py` (production style), `python -m uvicorn` |
| 03 | Type hints | Four jobs | Validation, conversion, documentation, editor help |
| 03 | Type hints | Return type | The return annotation also validates and filters the response |
| 03 | IDE support | Tools | Pylance or PyCharm: autocomplete, inline errors, hover; `mypy` for strict checks |
| 03 | Errors | Shape | 422 with `detail`: list of `type`, `loc` (where: path, query, body), `msg`, `input` |
| 04 | REST | Resources | Plural nouns in URLs: `/items`, `/items/3`; no verbs |
| 04 | REST | Methods | GET read, POST create, PUT replace, PATCH change, DELETE remove |
| 04 | REST | Properties | GET is safe; GET, PUT, DELETE are idempotent; POST is not; stateless requests |
| 04 | REST | Status codes | 200, 201 Created, 204 No Content, 400, 401, 403, 404, 409, 422, 500, 503 |
| 04 | REST | In FastAPI | `status_code=201` on the decorator; `HTTPException` for errors; `Response(status_code=204)` |
| 05 | Path parameters | Syntax | `/users/{user_id}` and a function argument with a type hint |
| 05 | Path parameters | Order | A fixed path (`/users/me`) must be declared before a variable one |
| 05 | Path parameters | Special | `{file_path:path}` accepts slashes; an `Enum` limits the allowed values |
| 06 | Query parameters | Rule | Not in the path means query; a default means optional; no default means required |
| 06 | Query parameters | Optional | `q: str | None = None`; booleans accept true/false, 1/0, yes/no, on/off |
| 06 | Query parameters | Use | Pagination `skip` and `limit`, filters, flags |
| 07 | Validation | Tools | `Annotated[int, Path(ge=1)]`, `Annotated[str, Query(min_length=3)]` |
| 07 | Validation | Rules | `gt ge lt le`, `min_length max_length pattern`, `alias`, `deprecated`, `title`, `description` |
| 07 | Validation | Lists | `Annotated[list[str] | None, Query()]` for `?tag=a&tag=b` |
| 08 | Pydantic | Model | `class X(BaseModel)`; creating an object validates and converts; all errors are reported together |
| 08 | Pydantic | Field | `Field(ge=, le=, min_length=, alias=, default=)` |
| 08 | Pydantic | Validators | `@field_validator` (one field), `@model_validator(mode="after")` (whole model) |
| 08 | Pydantic | Dump and load | `model_dump`, `model_dump_json`, `model_validate`, `model_validate_json`, `model_copy` |
| 08 | Pydantic | Config | `ConfigDict(frozen=True, extra="forbid", strict=True)`; `model_json_schema()` |
| 08 | Pydantic | v1 to v2 | `dict` to `model_dump`, `parse_obj` to `model_validate`, `validator` to `field_validator`, `Config` to `model_config` |
| 09 | Request body | Rule | A Pydantic-model parameter is read from the JSON body |
| 09 | Request body | Mixing | Path, query and body in one function; two models need one JSON key per parameter |
| 09 | Request body | Plain values | `Body(...)` for a single value; `Body(embed=True)` wraps it in a key |
| 09 | Request body | Errors | `loc` starts with `body`; invalid JSON gives `json_invalid`; extra keys are ignored |
| 10 | Errors | `HTTPException` | `raise` it with `status_code`, `detail`, optional `headers` |
| 10 | Errors | Handlers | `@app.exception_handler(MyError)`; override `RequestValidationError` to change the 422 shape |
| 10 | Errors | Unhandled | 500 "Internal Server Error"; test with `TestClient(app, raise_server_exceptions=False)` |
| 10 | Settings | pydantic-settings | `BaseSettings` reads `APP_*` environment variables or `.env`, converts and validates; never commit secrets |