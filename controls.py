from fastapi import FastAPI, HTTPException
from models import Burger, burger_pydantic, burger_in_pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel


class Message(BaseModel):
    message: str


app = FastAPI()


@app.post("/burger/create")
async def burger_create(burger: burger_in_pydantic):
    burger_object = await Burger.create(**burger.dict(exclude_unset=True))
    return await burger_pydantic.from_tortoise_orm(burger_object)


@app.get("/burgers/{burger_id}", response_model=burger_in_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_burger(burger_id: int):
    return await burger_in_pydantic.from_queryset_single(Burger.get(id=burger_id))


@app.put("/burger/update/{burger_id}", response_model=burger_pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_burger(burger_id: int, burger: burger_in_pydantic):
    await Burger.filter(id=burger_id).update(**burger.dict(exclude_unset=True))
    return await burger_pydantic.from_queryset_single(Burger.get(id=burger_id))


@app.delete("/burger/remove/{burger_id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def remove_burger(burger_id: int):
    burger_to_remove = await Burger.filter(id=burger_id).delete()
    if not burger_to_remove:
        return HTTPException(statue=404, detail="Specified id doesn't match any burger in the store")
    return Message(message="Burger successfully removed")


register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
