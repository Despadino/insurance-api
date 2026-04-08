from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Status(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    age: int
    money: int
    health: int
    happiness: int
    annual_savings: int
    is_finish: bool