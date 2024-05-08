from pydantic import BaseModel


class SchemaCarBase(BaseModel):
    make_model: str
    year: int
    price_usd: int
    engine_cap: float
    transmission: str
    mileage: int
    fuel_type: str
    color: str
    body_type: str
    engine_type: str
    wheel_pos: str
    mileage: int
    city: str
    car_link: str


class SchemaCarCreate(SchemaCarBase):
    pass


class SchemaCarUpdate(SchemaCarBase):
    pass


class SchemaCarView(SchemaCarBase):
    pass
