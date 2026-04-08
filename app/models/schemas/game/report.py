from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from .status import Status

class Report(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    status: Status
    report: str



