Write the questions as # comments and your solutions as code, with a test_*.py using TestClient for each.

Write a /report page with a Jinja2 template that extends base.html and shows a table of 5 sensor readings (name, value, unit). Rows whose value is above a limit get a CSS class alert. Test the rows and the class.
Send <script>alert(1)</script> as a name and prove that it appears escaped. Then use the |safe filter on purpose, test the difference, and write in a comment why it is dangerous.
Mount a static/ folder with a CSS file and a small JavaScript file. Link both from a template with url_for. Test that both are served with the right content type. Then try to start the app with a folder that does not exist and read the error.
Build a /contact form (name, email, message). GET shows it, POST validates it (message at least 10 characters), shows errors on the same page with status 422, and redirects with 303 on success. Test all three paths.
Write a Pydantic form model for a device registration (serial, firmware_version matching ^\d+\.\d+\.\d+$, ports between 1 and 8) with Form(). Test a valid form, a bad version and an extra field.
Build an upload endpoint that accepts only .csv files under 50 KB, counts the rows, and saves the file under a safe name in uploads/. Test a normal file, a wrong type, a file one byte over the limit and the name ../x.csv.
Add an endpoint that accepts several image files and returns each name and size. Then change it to reject the whole request if one file has the wrong type. Test both behaviours.
Write a login that sets a session_id cookie (httponly, samesite="lax"), a /me route that reads it, and a /logout that deletes it. Test the cookie flags and the full cycle with one TestClient.
Write a route that requires an X-Request-Id header and echoes it back in a response header of the same name. Test a missing header, a valid one and the underscore conversion.
Write UserIn, UserOut and UserInternal (with a password_hash and an is_admin flag). Return UserInternal objects from the routes and prove with tests that only UserOut fields reach the client. Add a route using response_model_exclude_none.
Build an Order model with a Customer, a list of OrderLine models (each with a Product), and a dict[str, str] of metadata. Test one valid order, and a failing line to see the full loc. Return an order summary with a response model.
Write a get_db() dependency with yield, a get_current_user() that reads an API key and uses get_db(), and a route that uses both. In the tests, override get_db with a fake and get_current_user with a fixed user. Check the cleanup order with an events list.
Add FastAPI(dependencies=[Depends(rate_limit)]) where rate_limit allows 5 calls per client and then raises 429. Test the sixth call, and reset the counter in a fixture.
CORS: allow http://localhost:3000 only. Write the tests for an allowed origin, a blocked origin, and a preflight with Authorization as the requested header. Explain in a comment why a curl request to the blocked origin still returns 200.
Async: write a route that fetches three fake slow services with asyncio.gather and a route that does the same one after another. Measure both with time.perf_counter() in a test and print the difference (do not assert exact times). Then put a time.sleep(0.2) inside an async def route and, with two requests started together, explain what you see.
Background tasks: write POST /orders that returns 202 and logs “order received” and “email queued” in two background tasks. Test the order of the log lines. Write in a comment why a task that takes 10 minutes should not run as a background task.
Embedded exercise: write a firmware-update API: POST /firmware accepts a binary upload (max 2 MB, only application/octet-stream), checks a X-Checksum header (CRC32 or SHA-256 of the body), saves it under a safe name, and returns 202 with an id. A background task “flashes” it (appends to a list). Add an X-API-Key dependency, a response model, and at least 12 tests including overrides.
Predict first, then run, and explain each result:
python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
calls = []

def a():
    calls.append("a")
    return 1

def b(x: Annotated[int, Depends(a)]):
    calls.append("b")
    return x + 1

@app.get("/")
def root(x: Annotated[int, Depends(a)], y: Annotated[int, Depends(b)]):
    return {"x": x, "y": y, "calls": calls}

print(TestClient(app).get("/").json())