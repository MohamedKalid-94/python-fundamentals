from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

# NESTED MODELS: a field can itself be a model, a list of models, a set, or a dict.
# FastAPI and Pydantic then validate the WHOLE tree, and an error tells you the exact path:
#   ["body", "items", 1, "price"]     = the "price" of the second element of "items"
#
#   images: list[Image] | None = None     a list of models
#   tags: set[str] = set()                a set: duplicates disappear (sent as a JSON list)
#   url: HttpUrl                          a special type: must be a valid web address
#   weights: dict[int, float]             a body with arbitrary keys; JSON keys are text, so "1" becomes 1
# Other useful types: UUID, datetime, date, Decimal, EmailStr (needs email-validator), Literal["a", "b"].

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    price: float
    tags: set[str] = set()
    images: list[Image] | None = None


class Offer(BaseModel):
    name: str
    items: list[Item]


@app.post("/items")
def create_item(item: Item):
    return {
        "name": item.name,
        "tag_count": len(item.tags),
        "image_names": [image.name for image in (item.images or [])],
    }


@app.post("/offers")
def create_offer(offer: Offer):
    return {"name": offer.name, "total": sum(item.price for item in offer.items), "items": len(offer.items)}


@app.post("/weights")
def weights(weights: dict[int, float]):
    return {"total": sum(weights.values()), "keys": sorted(weights)}


@app.get("/sample", response_model=Offer)           # nested models work in responses too
def sample():
    return Offer(name="sample", items=[Item(name="x", price=2, tags={"t"})])