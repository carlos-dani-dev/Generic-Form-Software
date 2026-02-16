from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import Survey, SurveyStatus, Question, Answer, Response

from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix='/response',
    tags=['response']
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
templates = Jinja2Templates(directory="App/templates")


class ResponseRequest(BaseModel):
    city: str = Field(min_length=3)
    begin_date: datetime
    end_date: Optional[datetime] = None


### PAGES ###

### ENDPOINTS ###

@router.get("/{survey_id}", status_code=status.HTTP_200_OK)
async def get_all_response(db: db_dependency, survey_id: int = Path(gt=0)):
    
    survey_model = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if survey_model is None: raise HTTPException(status_code=404, detail="Survey not found.")
    
    response_model = db.query(Response).filter(Response.survey_id == survey_id).all()
    return response_model

@router.get("/latest_response/{survey_id}", status_code=status.HTTP_200_OK)
async def get_latest_response(db: db_dependency, survey_id: int = Path(gt=0)):

    survey_model = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if survey_model is None: raise HTTPException(status_code=404, detail="Survey not found.")

    last_response_model = db.query(Response).filter(Response.survey_id == survey_id).order_by(Response.begin_date.desc()).first()
    return last_response_model

@router.post("/create/{survey_id}", status_code=status.HTTP_201_CREATED)
async def create_response(db: db_dependency, response_request: ResponseRequest,
                          survey_id: int = Path(gt=0)):
    
    survey_model = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if survey_model is None: raise HTTPException(status_code=404, detail="Survey not found.")
    
    response_model = Response(**response_request.model_dump(), survey_id=survey_id)
    
    db.add(response_model)
    db.commit()
    db.refresh(response_model)
    
    return {"response_id": response_model.response_id}


@router.delete("/delete/{response_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_response(db: db_dependency, survey_id: int = Path(gt=0), response_id: int = Path(gt=0)):
    
    response_model = db.query(Response).filter(Response.response_id == response_id).first()
    if response_model is None: raise HTTPException(status_code=404, detail="Response not found.")

    db.query(Response).filter(Response.response_id == response_id).first().delete()
    db.commit()