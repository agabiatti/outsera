from pydantic import BaseModel

class ProducerCreate(BaseModel):
    name: str

class ProducerOut(ProducerCreate):
    id: int

    model_config = {
        "from_attributes": True
    }