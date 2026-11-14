from fastapi import FastAPI

# FastAPI reads the TYPE HINTS of your function and uses them for FOUR jobs at once:
#   1. VALIDATION    "abc" is not an int: the client gets a 422 error, your code never runs
#   2. CONVERSION    the text "21" in the URL becomes the int 21 before your function starts
#   3. DOCUMENTATION the types appear in /docs and in openapi.json
#   4. EDITOR HELP   autocomplete and error checks while you type (below)
# Compare with Flask: number = int(request.args["number"]) by hand, plus your own error handling.
#
# The return annotation (-> dict[str, int]) is also used: FastAPI validates and filters the
# RESPONSE with it (Module 23, response models).
#
# IDE SUPPORT (VS Code with the Python and Pylance extensions, or PyCharm)
#   - autocomplete: type "number." and the editor lists int methods, because it knows the type
#   - inline errors: number.upper() is underlined, int has no upper()
#   - hover: shows the type and the docstring
#   - rename a variable or parameter safely, jump to a definition
#   - for stricter checks run  mypy app_03_type_hints_and_ide.py   (Module 20, file 04)
# The hints cost nothing at run time for plain Python, but here they DRIVE the framework.

app = FastAPI()


@app.get("/double/{number}")
def double(number: int) -> dict[str, int]:
    return {"result": number * 2}


@app.get("/greet")
def greet(name: str, excited: bool = False) -> dict[str, str]:
    text = f"Hello {name}"
    if excited:
        text += "!"
    return {"message": text}


# A bad request never reaches your function. The client receives (shortened):
#   GET /double/abc   ->   422
#   {"detail": [{"type": "int_parsing", "loc": ["path", "number"],
#                "msg": "Input should be a valid integer, unable to parse string as an integer",
#                "input": "abc"}]}
#   "loc" says WHERE the problem is: path, query, header, cookie or body, and the parameter name.