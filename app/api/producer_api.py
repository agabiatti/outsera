from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers.producer_controller import ProducerController
from app.schemas.producer_schema import ProducerCreate, ProducerOut
from app.connections.db import get_db

router = APIRouter(prefix="/producers", tags=["Producers"])

@router.get("/intervals")
def get_intervals(db: Session = Depends(get_db)):
    producer_controller = ProducerController(db)
    return producer_controller.get_producer_intervals()

@router.post("/", response_model=ProducerOut)
def create_producer(producer: ProducerCreate, db: Session = Depends(get_db)):
    result = ProducerController(db).create_producer(producer)
    
    return result

@router.get("/", response_model=list[ProducerOut])
def read_producers(db: Session = Depends(get_db)):
    results = ProducerController(db).read_producers()

    if results:
        return results

    raise HTTPException(status_code=404, detail="Producers not found")

@router.get("/{producer_id}", response_model=ProducerOut)
def read_producer(producer_id: int, db: Session = Depends(get_db)):
    result = ProducerController(db).read_producer(producer_id)

    if result:
        return result
    
    raise HTTPException(status_code=404, detail="Producer not found")

@router.put("/{producer_id}", response_model=ProducerOut)
def update_producer(producer_id: int, producer: ProducerCreate, db: Session = Depends(get_db)):
    result = ProducerController(db).update_producer(producer_id, producer)
    
    if result:
        return result

    raise HTTPException(status_code=404, detail="Producer not found")

@router.delete("/{producer_id}")
def delete_producer(producer_id: int, db: Session = Depends(get_db)):
    result = ProducerController(db).update_producer(producer_id)

    if result:
        return {"message": "Producer deleted"}
    
    raise HTTPException(status_code=404, detail="Producer not found")