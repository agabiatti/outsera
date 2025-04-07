from sqlalchemy.orm import Session
from app.models.studio import Studio

class StudioController():
    def __init__(self, db: Session):
        self.db = db

    def create_studio(self, studio):
        db_studio = Studio(**studio.model_dump())
        self.db.add(db_studio)
        self.db.commit()
        self.db.refresh(db_studio)
        return db_studio
    
    def read_studios(self):
        return self.db.query(Studio).all()
    
    def read_studio(self, studio_id):
        return self.db.get(Studio, studio_id)
    
    def update_studio(self, studio_id, studio):
        db_studio = self.db.get(Studio, studio_id)
        
        if not db_studio:
            return None
        
        for key, value in studio.model_dump().items():
            setattr(db_studio, key, value)
        
        self.db.commit()
        self.db.refresh(db_studio)

        return db_studio
    
    def delete_studio(self, studio_id):
        db_studio = self.db.get(Studio, studio_id)
        
        if not db_studio:
            return False
        
        self.db.delete(db_studio)
        self.db.commit()

        return True
        