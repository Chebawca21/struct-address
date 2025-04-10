from typing import Union
from pydantic import BaseModel, Field, SerializeAsAny
from enum import Enum

class Address(BaseModel):
    '''Polish name and address of a person'''

    name: Union[str, None] = Field(description="Name and surname of the person")
    street: Union[str, None] = Field(description="Name of the street")
    house_number: Union[str, None] = Field(description="House number")
    postcode: Union[str, None] = Field(description="Polish postcode")
    city: Union[str, None] = Field(description="Name of the city, if no city name is provided deduce it from postcode")
    voivodeship: Union[str, None] = Field(description="Voivodeship, if none is provided deduce it from city or postcode")

class Status(str, Enum):
    unknown = "UNKNOWN"
    pending = "PENDING"
    done = "DONE"

class Process(BaseModel):
    uuid: int
    status: Status = Status.unknown
    address: SerializeAsAny[Union[Address, None]] = None
