from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel



class Read(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,  
        populate_by_name=True,
    )

    id: UUID
    user_id: UUID

    full_name: str
    
    is_finish:bool