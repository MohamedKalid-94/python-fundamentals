import itertools
import os
from functools import lru_cache
from typing import Annotated, Protocol

from fastapi import Depends, FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

# MONGODB stores DOCUMENTS (JSON-like, binary-encoded as BSON) in COLLECTIONS, inside a DATABASE.
#   table -> collection      row -> document      column -> field
#   no fixed schema, nested data is natural, every document has an _id (an ObjectId by default).
# Good for: variable or nested data, chat history, LLM outputs, caches of raw documents.
# Use Pydantic to keep the SHAPE of what you store under control: the database will not do it for you.
#
# ASYNC DRIVER: use the PyMongo async API:  from pymongo import AsyncMongoClient
#   every call that touches the network is awaited; find() is NOT awaited and returns a cursor
#   you loop over with "async for" (or await cursor.to_list()).
#   Install: pip install pymongo      Start a local server: docker run -d -p 27017:27017 mongo
#   Then:    $env:MONGODB_URL = "mongodb://localhost:27017" ; fastapi dev app_03_mongodb.py
#
# DESIGN: the endpoints talk to a "store" with 4 methods (a Protocol). Two implementations:
#   MongoNoteStore       the real database (not run by the tests)
#   InMemoryNoteStore    a fake with the same methods (used by the tests, and by default)
# The tests swap the store with dependency_overrides, so they need no server.


class NoteIn(BaseModel):
    title: str = Field(min_length=1)
    body: str = ""


class NoteOut(NoteIn):
    id: str                                     # an ObjectId is sent as text


class NoteStore(Protocol):
    async def create(self, data: dict) -> str: ...
    async def get(self, note_id: str) -> dict | None: ...
    async def get_many(self, limit: int) -> list[dict]: ...
    async def delete(self, note_id: str) -> bool: ...


class InMemoryNoteStore:
    def __init__(self):
        self.notes: dict[str, dict] = {}
        self._counter = itertools.count(1)

    async def create(self, data: dict) -> str:
        note_id = str(next(self._counter))
        self.notes[note_id] = dict(data)
        return note_id

    async def get(self, note_id: str) -> dict | None:
        note = self.notes.get(note_id)
        return {"id": note_id, **note} if note is not None else None

    async def get_many(self, limit: int) -> list[dict]:
        return [{"id": note_id, **note} for note_id, note in list(self.notes.items())[:limit]]

    async def delete(self, note_id: str) -> bool:
        return self.notes.pop(note_id, None) is not None


class MongoNoteStore:
    def __init__(self, url: str, database: str = "course"):
        from pymongo import AsyncMongoClient            # imported here: only needed with a real MongoDB
        self.client = AsyncMongoClient(url)
        self.notes = self.client[database]["notes"]

    @staticmethod
    def _object_id(note_id: str):
        from bson import ObjectId
        from bson.errors import InvalidId
        try:
            return ObjectId(note_id)
        except InvalidId:
            return None

    @staticmethod
    def _to_dict(document: dict) -> dict:
        document["id"] = str(document.pop("_id"))       # ObjectId -> text
        return document

    async def create(self, data: dict) -> str:
        result = await self.notes.insert_one(dict(data))
        return str(result.inserted_id)

    async def get(self, note_id: str) -> dict | None:
        object_id = self._object_id(note_id)
        if object_id is None:
            return None
        document = await self.notes.find_one({"_id": object_id})
        return self._to_dict(document) if document else None

    async def get_many(self, limit: int) -> list[dict]:
        cursor = self.notes.find().limit(limit)         # not awaited: it returns an async cursor
        return [self._to_dict(document) async for document in cursor]

    async def delete(self, note_id: str) -> bool:
        object_id = self._object_id(note_id)
        if object_id is None:
            return False
        result = await self.notes.delete_one({"_id": object_id})
        return result.deleted_count == 1


@lru_cache
def get_store() -> NoteStore:
    url = os.environ.get("MONGODB_URL")
    return MongoNoteStore(url) if url else InMemoryNoteStore()


StoreDep = Annotated[NoteStore, Depends(get_store)]

app = FastAPI()


@app.post("/notes", response_model=NoteOut, status_code=201)
async def create_note(note: NoteIn, store: StoreDep):
    note_id = await store.create(note.model_dump())
    return {"id": note_id, **note.model_dump()}


@app.get("/notes", response_model=list[NoteOut])
async def list_notes(store: StoreDep, limit: int = 10):
    return await store.get_many(limit)


@app.get("/notes/{note_id}", response_model=NoteOut)
async def read_note(note_id: str, store: StoreDep):
    note = await store.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@app.delete("/notes/{note_id}", status_code=204)
async def delete_note(note_id: str, store: StoreDep):
    if not await store.delete(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return Response(status_code=204)