from pydantic import BaseModel

class StudioCreate(BaseModel):
    name: str

class StudioOut(StudioCreate):
    id: int

    model_config = {
        "from_attributes": True
    }