from dataclasses import dataclass
from fastapi import Form
from typing import Annotated
from pydantic import BaseModel
from datetime import date
from enum import StrEnum


class ItemType(StrEnum):
    food = "food"
    fridge = "fridge"
    cleaning = "cleaning"


@dataclass
class ItemForm:
    name: Annotated[str, Form()]
    item_type: Annotated[ItemType, Form()]


class Unit(StrEnum):
    grams = "g"
    kilograms = "kg"
    liters = "L"
    mililiters = "mL"
    pieces = "pieces"


class Package(BaseModel):
    package_size: float
    package_size_unit: Unit


class Item(BaseModel):
    name: str
    item_type: str  # TODO: make this an enum (food, fridge, cleaning stuff...)
    expiration_date: date | None
    package: Package | None
