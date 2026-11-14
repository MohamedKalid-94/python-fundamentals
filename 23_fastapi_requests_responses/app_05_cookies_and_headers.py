from typing import Annotated

from fastapi import Cookie, FastAPI, Header, Response

# COOKIES and HEADERS are read the same way as query parameters, with Cookie() and Header().
#
# COOKIE: a small value the browser stores and sends back with every request to your site
#   session_id: Annotated[str | None, Cookie()] = None
#   response.set_cookie(key, value, httponly=True, secure=True, samesite="lax", max_age=3600)
#       httponly   JavaScript cannot read it (protects against script theft)
#       secure     sent only over HTTPS
#       samesite   limits sending it from other sites (helps against cross-site request forgery)
#       max_age    lifetime in seconds
#   response.delete_cookie(key)
#
# HEADER: extra information about the request or response
#   user_agent: Annotated[str | None, Header()] = None
#   FastAPI converts the Python name to the header name:  x_token  <->  X-Token  (case does not matter)
#   Header(convert_underscores=False) keeps underscores. A header sent twice -> list[str].
#   To ADD a header to the answer, change response.headers.
#   In the error list the location is ["header", "<name>"]; the name may be shown with a hyphen.

app = FastAPI()


@app.get("/me")
def me(session_id: Annotated[str | None, Cookie()] = None):
    return {"session_id": session_id}


@app.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="session_id", value="abc123", httponly=True, samesite="lax", max_age=3600)
    return {"message": "cookie set"}


@app.get("/delete-cookie")
def delete_cookie(response: Response):
    response.delete_cookie("session_id")
    return {"message": "cookie removed"}


@app.get("/agent")
def agent(user_agent: Annotated[str | None, Header()] = None):
    return {"user_agent": user_agent}


@app.get("/token")
def token(x_token: Annotated[str, Header()]):
    return {"x_token": x_token}


@app.get("/tokens")
def tokens(x_token: Annotated[list[str] | None, Header()] = None):
    return {"x_token": x_token}


@app.get("/custom-header")
def custom_header(response: Response):
    response.headers["X-Process-Time"] = "0.01"
    return {"ok": True}