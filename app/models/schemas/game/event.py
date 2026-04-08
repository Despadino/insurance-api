from pydantic import BaseModel, ConfigDict, field_serializer
from pydantic.alias_generators import to_camel

class Event(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
    )

    title: str
    description: str
    image: bytes


    @field_serializer("image")
    def serialize_image(self, image: bytes, _info):
        """Преобразуем bytes в base64 строку с префиксом data:image/..."""
        import base64
        import imghdr
        mime_type = "image/png"
        encoded = base64.b64encode(image).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"