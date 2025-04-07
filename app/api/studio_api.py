from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers.studio_controller import StudioController
from app.schemas.studio_schema import StudioCreate, StudioOut
from app.connections.db import get_db

router = APIRouter(prefix="/studios", tags=["Studios"])

@router.post("/", response_model=StudioOut)
def create_studio(studio: StudioCreate, db: Session = Depends(get_db)):
    result = StudioController(db).create_studio(studio)
    
    return result

@router.get("/", response_model=list[StudioOut])
def read_studios(db: Session = Depends(get_db)):
    results = StudioController(db).read_studios()

    if len(results) > 0:
        return results

    raise HTTPException(status_code=404, detail="Studios not found")

@router.get("/{studio_id}", response_model=StudioOut)
def read_studio(studio_id: int, db: Session = Depends(get_db)):
    result = StudioController(db).read_studio(studio_id)

    if result:
        return result

    raise HTTPException(status_code=404, detail="Studio not found")

@router.put("/{studio_id}", response_model=StudioOut)
def update_studio(studio_id: int, studio: StudioCreate, db: Session = Depends(get_db)):
    result = StudioController(db).update_studio(studio_id, studio)
    
    if result:
        return result

    raise HTTPException(status_code=404, detail="Studio not found")

@router.delete("/{studio_id}")
def delete_studio(studio_id: int, db: Session = Depends(get_db)):
    result = StudioController(db).update_studio(studio_id)

    if result:
        return {"message": "Studio deleted"}
    
    raise HTTPException(status_code=404, detail="Studio not found")