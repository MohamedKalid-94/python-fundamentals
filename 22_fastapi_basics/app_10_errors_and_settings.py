from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings, SettingsConfigDict

# ---------- ERRORS ----------
# 1. HTTPException: stop the function and send an error response.
#      raise HTTPException(status_code=404, detail="Sensor not found")   ->  {"detail": "Sensor not found"}
#    Use "raise", not "return". You may add headers=...
# 2. Your own exception + a handler: turn a domain error into a response in ONE place.
# 3. Override the handler for RequestValidationError to change the shape of 422 errors.
# 4. Anything unhandled becomes 500 "Internal Server Error" (the traceback stays in the server log).
# Pick the code that matches the cause:  400 your input is wrong, 401/403 who you are, 404 not found,
# 409 conflict, 422 validation, 429 too many requests, 5xx the server is at fault.

app = FastAPI()


class SensorOffline(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(SensorOffline)
async def sensor_offline_handler(request: Request, exc: SensorOffline):
    return JSONResponse(status_code=503, content={"error": f"sensor {exc.name} is offline"})


@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    problems = [
        {"field": ".".join(str(part) for part in error["loc"][1:]), "message": error["msg"]}
        for error in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"errors": problems})


@app.get("/sensors/{name}")
def read_sensor(name: str):
    if name == "broken":
        raise SensorOffline(name)
    if name == "missing":
        raise HTTPException(status_code=404, detail="Sensor not found", headers={"X-Error": "no-sensor"})
    return {"name": name, "value": 21.5}


@app.get("/double/{number}")
def double(number: int):
    return {"result": number * 2}


@app.get("/crash")
def crash():
    raise RuntimeError("boom")                  # not handled: the client gets a 500


# ---------- SETTINGS (pydantic-settings) ----------
# Configuration comes from ENVIRONMENT VARIABLES (or a .env file), never from values written in the code.
# BaseSettings is a Pydantic model that reads them, converts the types, and validates them.
#   APP_NAME=demo   APP_DEBUG=true   APP_MAX_ITEMS=5      (names are not case sensitive)
# API keys and passwords belong here too. Never commit a .env file (it is in .gitignore).
# Module 23 shows how to share one Settings object with Depends.


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

    name: str = "my-api"
    debug: bool = False
    max_items: int = 100