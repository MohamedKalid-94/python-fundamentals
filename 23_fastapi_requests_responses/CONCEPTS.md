# Module 23: FastAPI Requests and Responses, Concepts Summary

| # | Topic | Concept | Remember |
|---|---|---|---|
| 01 | Templates | Jinja2 | `Jinja2Templates(directory=...)`, `TemplateResponse(request=, name=, context=)`; build the folder path from `__file__` |
| 01 | Templates | Syntax | `{{ x }}` print (auto-escaped), `{% for %}`, `{% if %}`, `{% extends %}` with `{% block %}` |
| 01 | Templates | Security | Auto-escaping stops script injection; never turn it off for user text |
| 02 | Static files | Mount | `app.mount("/static", StaticFiles(directory=...), name="static")`; `url_for('static', path='/x.css')` in templates |
| 02 | Static files | Behaviour | Missing folder is a start-up error; `../` tricks give 404; mounted apps are not in `/docs` |
| 03 | Forms | HTML form | `<form method="post">` sends `application/x-www-form-urlencoded`; needs `python-multipart` |
| 03 | Forms | Read data | `Annotated[str, Form()]`; a whole form as one Pydantic model with `Annotated[Model, Form()]` |
| 03 | Forms | Flow | GET shows the form, POST handles it, success redirects with 303 (post, redirect, get) |
| 03 | Forms | Limit | A route takes form data or JSON, not both |
| 04 | Uploads | Types | `Annotated[bytes, File()]` (small), `UploadFile` (large), `list[UploadFile]` (several) |
| 04 | Uploads | `UploadFile` | `.filename`, `.content_type`, `await .read(n)`; copy in chunks |
| 04 | Uploads | Safety | Keep `Path(name).name`, check type (415), limit size (413), never trust the client's content type |
| 05 | Cookies | Read and write | `Annotated[str | None, Cookie()]`; `response.set_cookie(httponly, secure, samesite, max_age)`; `delete_cookie` |
| 05 | Headers | Read | `Header()` converts `x_token` to `X-Token`; a repeated header is `list[str]`; `convert_underscores=False` |
| 05 | Headers | Write | `response.headers["X-..."] = ...` |
| 06 | Response model | Purpose | Filters secrets out, converts and validates output, documents the answer |
| 06 | Response model | Patterns | Separate `UserIn` and `UserOut`; `response_model=list[X]`; `response_model_exclude_unset`, `exclude_none` |
| 06 | Response model | Bad output | A mismatch is a 500 error, not wrong data for the client |
| 07 | Nested models | Shapes | Model in model, `list[Model]`, `set[str]` (no duplicates), `dict[int, float]`, `HttpUrl` |
| 07 | Nested models | Errors | `loc` is the exact path, for example `["body", "items", 1, "price"]` |
| 08 | Dependencies | Idea | `Depends(function)`: FastAPI builds the value and injects it; sub-dependencies are allowed |
| 08 | Dependencies | Forms | Function, class (`Depends()`), `yield` (cleanup), `dependencies=[...]` in the decorator |
| 08 | Dependencies | Caching | The same dependency runs once per request; `use_cache=False` runs it each time |
| 08 | Dependencies | Testing | `app.dependency_overrides[original] = replacement`; clear it after each test |
| 08 | Dependencies | Settings | `@lru_cache` on `get_settings()` creates the settings once |
| 09 | CORS | Meaning | A browser rule about origins (scheme, host, port); the server only sends permission headers |
| 09 | CORS | Setup | `CORSMiddleware(allow_origins, allow_credentials, allow_methods, allow_headers, max_age)` |
| 09 | CORS | Preflight | OPTIONS request before non-simple calls; a disallowed origin, method or header gets 400 |
| 09 | CORS | Warning | It is not API security: curl still gets answers; no `"*"` together with credentials |
| 10 | Async | `def` vs `async def` | `def` runs in a thread pool (blocking is OK); `async def` runs on the event loop (never block) |
| 10 | Async | Tools | `await asyncio.gather(...)`, `await asyncio.to_thread(func, ...)` |
| 10 | Background tasks | Use | `BackgroundTasks.add_task(func, ...)` runs after the response; return 202; use a queue for heavy work |