from collections.abc import Iterator
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.pool import StaticPool

# SQLALCHEMY 2.0 is the standard Python toolkit for SQL databases (you used raw SQL with sqlite3 in Module 18).
#   ENGINE   the connection pool to one database (a URL says which: sqlite://, postgresql+psycopg://...)
#   MODEL    a Python class mapped to a table (the ORM: object-relational mapper)
#   SESSION  a unit of work: add, change, delete, then commit() or rollback()
# THE FASTAPI PATTERN: one session PER REQUEST, from a yield dependency (Module 23, lesson 08).
#   - two kinds of model: ORM models (tables) and Pydantic models (what goes in and out)
#   - ConfigDict(from_attributes=True) lets a Pydantic model read an ORM object
#   - a def endpoint with this ordinary (blocking) session runs in the thread pool: that is fine
#   - the database stays the SAME when you change SQLite to PostgreSQL: only the URL changes
# Alembic creates and migrates tables in a real project; create_all below is for learning.
# RUN: fastapi dev app_02_sql_database.py   (creates devices.db here; *.db is in .gitignore)

DATABASE_URL = "sqlite:///./devices.db"


def make_engine(url: str):
    if not url.startswith("sqlite"):
        return create_engine(url)
    options = {"connect_args": {"check_same_thread": False}}      # SQLite: allow use from several threads
    if url in ("sqlite://", "sqlite:///:memory:"):
        options["poolclass"] = StaticPool                         # in-memory: keep ONE shared connection
    return create_engine(url, **options)


engine = make_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    firmware: Mapped[str] = mapped_column(String(20), default="1.0.0")
    online: Mapped[bool] = mapped_column(default=False)


class DeviceCreate(BaseModel):
    name: str
    firmware: str = "1.0.0"


class DeviceRead(DeviceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    online: bool


class OnlineUpdate(BaseModel):
    online: bool


def get_db() -> Iterator[Session]:
    with SessionLocal() as session:             # closed after the request, even after an error
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)            # create the tables at start-up (lesson 06 explains lifespan)
    yield


app = FastAPI(lifespan=lifespan)


def get_device_or_404(db: Session, device_id: int) -> Device:
    device = db.get(Device, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return device


@app.post("/devices", response_model=DeviceRead, status_code=201)
def create_device(data: DeviceCreate, db: SessionDep):
    device = Device(**data.model_dump())
    db.add(device)
    try:
        db.commit()
    except IntegrityError:                      # the UNIQUE constraint on name
        db.rollback()
        raise HTTPException(status_code=409, detail="Device name already exists")
    db.refresh(device)
    return device


@app.get("/devices", response_model=list[DeviceRead])
def list_devices(
    db: SessionDep,
    online: bool | None = None,
    skip: int = 0,
    limit: Annotated[int, Query(le=100)] = 10,
):
    query = select(Device).order_by(Device.id).offset(skip).limit(limit)
    if online is not None:
        query = query.where(Device.online == online)
    return db.scalars(query).all()


@app.get("/devices/{device_id}", response_model=DeviceRead)
def read_device(device_id: int, db: SessionDep):
    return get_device_or_404(db, device_id)


@app.patch("/devices/{device_id}/online", response_model=DeviceRead)
def set_online(device_id: int, update: OnlineUpdate, db: SessionDep):
    device = get_device_or_404(db, device_id)
    device.online = update.online
    db.commit()
    return device


@app.delete("/devices/{device_id}", status_code=204)
def delete_device(device_id: int, db: SessionDep):
    device = get_device_or_404(db, device_id)
    db.delete(device)
    db.commit()
    return Response(status_code=204)


# TESTING: override get_db with a session on an in-memory database (see the test file).
# Never let tests touch your real database file.