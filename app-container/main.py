from fastapi import FastAPI, HTTPException, Form
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(title="Burger delivery service", version="v0.1.0")

store_burgers = []


class Burger(BaseModel):
    id: int
    name: str
    weight: float
    commanditor: str


class Login(BaseModel):
    username: str
    password: str


class BurgerAddResponseModel(BaseModel):
    name: str
    weight: float
    commanditor: str


class BurgerSearchModel(BaseModel):
    ID: str
    name: str
    weight: float


@app.get("/")
async def home():
    return {
        "message": "Burger delivery service. You're welcome"
    }


@app.get("/burgers/", response_model=List[Burger])
async def get_burgers():
    return store_burgers


@app.get("/burgers/{burger_id}/", response_model=Burger)
async def get_burger(burger_id: int):
    try:
        return store_burgers[burger_id]
    except:
        raise HTTPException(
            status_code=404, detail="Specified ID doesn't match any burger in the store")


@app.get("/burgers/search", response_model=BurgerSearchModel, response_model_exclude={'name'})
async def burger_search(name: str, weight: Optional[float]):
    return {
        "id": name + str(weight),
        "name": name,
        "weight": weight
    }

# POST


@app.post("/burgers/add/{commanditor}/", response_model=BurgerAddResponseModel, response_model_exclude={'name'})
async def burger_create(commanditor: str, new_burger: Burger):
    store_burgers.append(new_burger)
    return new_burger.dict()


@app.put("/burger/change/{burger_id}/", response_model=Burger)
async def update_burger(burger_id: int, new_burger: Burger):
    try:
        store_burgers[burger_id] = new_burger
        return store_burgers[burger_id]
    except:
        raise HTTPException(
            status_code=404, detail="Specified ID doesn't match any burger in the store")


@app.delete("/burger/delete/{burger_id}", response_model=Burger)
async def delete_burger(burger_id: int):
    try:
        burger_object = store_burgers[burger_id]
        store_burgers.pop(burger_id)
        return burger_object
    except:
        raise HTTPException(
            status_code=404, detail="Specified ID doesn't match any burger in the store")


@app.post("/admin/login/", response_model=Login)
async def login(username: str = Form(...), password: str = Form(...)):
    return {
        "username": username,
        "password": password
    }
