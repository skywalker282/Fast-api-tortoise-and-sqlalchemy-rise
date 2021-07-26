from typing import List

from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import databases
import sqlalchemy
from datetime import datetime

DATABASE_URL = "sqlite:///store.db"

metadata = sqlalchemy.MetaData()

database = databases.Database(DATABASE_URL)

register = sqlalchemy.Table(
    "register",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True), sqlalchemy.Column(
        "name", sqlalchemy.String(250)), sqlalchemy.Column("created_at", sqlalchemy.DateTime())
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={
    "check_same_thread": False})

app = FastAPI()


@app.on_event("shutdown")
async def connect():
    await database.disconnect()


class Register(BaseModel):
    id: int
    name: str
    created_at: datetime


class RegisterIn(BaseModel):
    name: str = Field(...)


@app.post("/register/", response_model=Register)
async def create_customer(customer: RegisterIn = Depends()):
    query = Register.insert().values(name=customer.name, created_at=datetime.utcnow())
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == record_id)
    row = await database.fetch_one(query)
    return {**row}


@app.get("/registers/", response_model=List[Register])
async def get_customers():
    query = register.select()
    customers = await database.fetch_all(query)
    return customers


@app.get("/customers/{customer_id}", response_model=Register)
async def get_customer(customer_id: int):
    query = register.select().where(register.c.id == customer_id)
    user = await database.fetch_one(query)
    return {**user}


@app.put("/register/{customer_id}", response_model=Register)
async def update_customer(customer_id: int, customer: RegisterIn = Depends()):
    query = register.update().where(register.c.id == customer_id).values(
        name=customer.name, created_at=datetime.utcnow())
    record_id = await database.execute(query)
    query = register.select().where(register.c.id == customer_id)
    row = await database.fetch_one(query)
    return {**row}


@app.delete("/register/{id}", response_model=Register)
async def delete(customer_id: int):
    query: register.delete().where(register.c.id == id)
    return await database.execute(query)
