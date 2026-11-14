Write the questions as # comments and your solutions as code. For each one, build the app and a test_*.py for it with TestClient.

Write an app with / (returns the app name and version) and /about. Test the 200 answers, one 404 and one 405.
Give your app a title, description, version and two tags. Test that /openapi.json shows them. Create a second app with docs switched off and test that /docs gives 404.
Start an app with uvicorn ... --port 9000, then with --workers 2. Why can --reload not be combined with --workers? Write the answer in a comment.
Write /add/{a}/{b} for ints and /area with width: float and height: float as query parameters. Test the 422 errors and check loc and type. Add a wrong-type mistake on purpose and see what mypy says.
Build a /books resource in memory with GET list, GET one, POST (201), PUT, DELETE (204) and 404 for a missing book, taking the title from the query string. Reset the data in a fixture.
Write /devices/{device_id}/channels/{channel} where channel is an Enum (a, b, c), and /logs/{path:path}. Test a valid channel, an invalid channel and a path with slashes.
Write /readings with skip, limit, and a sort Enum (asc, desc), over a list of 20 readings. Test paging at the edges (skip past the end gives an empty list).
Add validation: limit between 1 and 50, device_id >= 1, and a mac query parameter that must match ^([0-9A-F]{2}:){5}[0-9A-F]{2}$. Add a tag list parameter. Test one failing case for each rule.
Write a SensorReading Pydantic model: sensor_id (int, positive), celsius (-50 to 150), unit (only "C" or "F" with a field_validator), and a model_validator that rejects a Fahrenheit reading below -58 or above 302. Test model_dump, model_dump_json, model_validate_json and a failing JSON string.
Write POST /readings (returns 201) that takes a SensorReading body, stores it, and returns it with an id. Then write POST /readings/batch that takes list[SensorReading] as the body. Test both, including a batch where one item is invalid, and look at its loc.
Write PUT /devices/{device_id} that mixes a path parameter, a query parameter dry_run and a body model. Test every combination of present and missing values.
Add HTTPException (404 and 409), a custom DeviceBusy exception with a handler that returns 409 and a Retry-After header, and a custom 422 format. Test each one, and test that an unhandled error gives 500.
Write a Settings class with env_prefix="GATEWAY_", a SecretStr API key, a port and a debug flag. Test the defaults and the environment values with monkeypatch. Show that printing the settings does not reveal the secret.
Embedded exercise: write an HTTP gateway for fake sensors: POST /sensors/{id}/readings (body: value and unit), GET /sensors/{id}/latest, GET /sensors/{id}/history?limit=10, and GET /health. Keep the data in memory, return the correct status codes, validate everything, and write at least 12 tests.
Predict first, then run, and explain each result in a comment:
python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

@app.get("/items/{item_id}")
def by_id(item_id: int):
    return {"id": item_id}

@app.get("/items/latest")
def latest():
    return {"id": "latest"}

client = TestClient(app)
print(client.get("/items/latest").status_code)
print(client.get("/items/5").json())
print(client.post("/items/5").status_code)
print(client.get("/items/5/").status_code)

Then fix the order problem and run it again.