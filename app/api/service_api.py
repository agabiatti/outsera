from fastapi import APIRouter, Body, HTTPException
from app.services.insert_data import load_data

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/load_data")
def post_data(csv_path: str = Body(..., embed=True)):
    result = load_data(csv_path)

    if result:
        return {"message": "Data loaded successfully"}
    
    raise HTTPException(status_code=500, detail="Error")