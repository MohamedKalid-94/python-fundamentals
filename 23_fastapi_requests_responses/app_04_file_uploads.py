from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

# FILE UPLOADS arrive as  multipart/form-data  (needs python-multipart).
#   file: Annotated[bytes, File()]     the whole file in memory: only for small files
#   file: UploadFile                   a file-like object: kept in memory up to a limit, then on disk
#       .filename  .content_type  .size   await file.read(n)   await file.seek(0)   await file.close()
#   files: Annotated[list[UploadFile], File()]       several files in one field
#   File fields and Form fields can be mixed; File fields and a JSON body cannot.
#
# NEVER TRUST AN UPLOAD
#   - the filename can contain folders ("../../x"): keep only the last part with Path(name).name
#   - content_type is what the client claims; check the real content when it matters
#   - limit the size: read in chunks, stop at a maximum (413 Payload Too Large)
#   - allow only the types you expect (415 Unsupported Media Type)
#   - never execute or serve uploaded files from a folder that the web server can run
# Send one from PowerShell:  curl.exe -F "file=@notes.txt;type=text/plain" http://127.0.0.1:8000/upload

app = FastAPI()

UPLOAD_DIR = Path(__file__).parent / "uploads"      # created on first use; ignored by Git
MAX_BYTES = 1_000_000
ALLOWED_TYPES = {"text/plain", "text/csv"}


@app.post("/upload/bytes")
def upload_bytes(file: Annotated[bytes, File()]):
    return {"size": len(file)}


@app.post("/upload")
async def upload(file: UploadFile):
    content = await file.read()
    return {"filename": file.filename, "content_type": file.content_type, "size": len(content)}


@app.post("/upload/many")
async def upload_many(files: Annotated[list[UploadFile], File()], description: Annotated[str, Form()] = ""):
    return {"names": [f.filename for f in files], "description": description}


@app.post("/upload/csv")
async def upload_csv(file: UploadFile):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Only text/plain or text/csv are accepted")
    content = await file.read(MAX_BYTES + 1)            # read one byte more than allowed
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large")
    return {"filename": file.filename, "lines": len(content.decode("utf-8").splitlines())}


@app.post("/upload/save", status_code=201)
async def save_file(file: UploadFile):
    UPLOAD_DIR.mkdir(exist_ok=True)
    safe_name = Path(file.filename or "upload.bin").name        # "../../evil.txt" becomes "evil.txt"
    target = UPLOAD_DIR / safe_name
    with target.open("wb") as out:
        while chunk := await file.read(64 * 1024):              # copy in 64 KB chunks
            out.write(chunk)
    return {"saved_as": safe_name, "size": target.stat().st_size}