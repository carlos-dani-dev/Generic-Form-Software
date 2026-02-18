from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import City


router = APIRouter(
    prefix='/city',
    tags=['city']
)


def get_db():
    """
    Abre uma nova conexão com o banco de dados e a retorna (yield)
    Após o fim do escopo em que a função get_db é chamada, a conexão é fechada
    """

    db = SessionLocal()
    try: yield db
    finally: db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class CityRequest(BaseModel):
    city_name: str = Field(min_length=3)


### PAGES ###

### ENDPOINTS ###

@router.get("/{city_id}", status_code=status.HTTP_200_OK)
async def get_city_name(db: db_dependency, city_id: int = Path(gt=0)):
    
    city_model = db.query(City).filter(City.city_id == city_id).first()
    if city_model is None: raise HTTPException(status_code=404, detail="City not found.")
    
    return city_model


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_city(db: db_dependency, city_request: CityRequest):
    
    city_model = City(**city_request.model_dump())
    
    db.add(city_model)
    db.commit()