from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status, Response

from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import Survey, SurveyStatus, Question, QuestionOption, City, Response, QuestionDependency

from jose import JWTError, jwt
from ..config import SECRET_KEY, ALGORITHM
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/survey',
    tags=['survey']
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


class SurveyStatusRequest(BaseModel):
    survey_status: str = Field(min_length=5)
    

class SurveyRequest(BaseModel):
    name: str = Field(min_length=5)
    description: str = Field(min_length=5, max_length=100)
    start_date: datetime 
    end_date: Optional[datetime] = None

class CityRequest(BaseModel):
    city: str=Field(min_length=3)

async def get_response_id(db: db_dependency, auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=[ALGORITHM])
        survey_id: int = payload.get('survey_id')
        response_id: int = payload.get('response_id')

        if survey_id is None or response_id is None:
            return None

        response_model = db.query(Response).filter(
            Response.response_id == response_id,
            Response.survey_id == survey_id
        ).first()

        if response_model is None:
            return None
        return int(response_id)
    except (JWTError, ValueError, TypeError):
        return None


def redirect_to_city_page(survey_id: int):
    redirect_response = RedirectResponse(url=f"/survey/city/{survey_id}", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="auth_token")
    print("caiu aqui 1")
    return redirect_response

### PAGES ###

@router.get("/city/{survey_id}")
async def render_city_code_page(request: Request, db: db_dependency, survey_id: int):
    cities = db.query(City).all()
    template_response = templates.TemplateResponse("city.html", {"request": request, "cities": cities})
    return template_response


@router.get("/fill/{survey_id}")
async def render_survey_response_page(request: Request,
        db: db_dependency, survey_id: int):
    
    
    auth_token = request.cookies.get("auth_token")
    response_id = await get_response_id(db, auth_token)

    if response_id is None:
        return redirect_to_city_page(survey_id)
    
    question_model = db.query(Question).filter(Question.survey_id == survey_id,
        Question.is_independent == True).order_by(Question.order).all()
    
    question_opt_list = []
    for question in question_model:
        question_opt_list.append(
            db.query(QuestionOption).filter(QuestionOption.question_id == question.question_id).order_by(QuestionOption.order).all()
        )
    question_opt_list = [x for _ in question_opt_list for x in _]
    
    dependencies = db.query(QuestionDependency).all()
    
    return templates.TemplateResponse("response.html", {"request": request,
            "questions": question_model, "questions_opt": question_opt_list, "dependencies": dependencies})
    
### ENDPOINTS ###

    
@router.get("/status", status_code=status.HTTP_200_OK)
async def get_all_survey_status(db: db_dependency):
    return db.query(SurveyStatus).all()


@router.post("/status/create", status_code=status.HTTP_201_CREATED)
async def create_survey_status(db: db_dependency, survey_status_request: SurveyStatusRequest):
    
    # pesquisa criada automaticamente com status_id = 0
    survey_status_model = SurveyStatus(**survey_status_request.model_dump())
    db.add(survey_status_model)
    db.commit()


@router.delete("/status/delete/{survey_status_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey_status(db: db_dependency, survey_status_id: int = Path(gt=0)):
    
    survey_status_model = db.query(SurveyStatus).filter(SurveyStatus.survey_status_id == survey_status_id).first()
    if survey_status_model is None: raise HTTPException(status_code=404, detail="Survey status not found.")
    
    db.query(SurveyStatus).filter(SurveyStatus.survey_status_id == survey_status_id).first().delete()
    db.commit()


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_surveys(db: db_dependency):
    return db.query(Survey).all()


@router.post("/create/{survey_status_id}", status_code=status.HTTP_201_CREATED)
async def create_survey(db: db_dependency, survey_request: SurveyRequest, survey_status_id: int = Path(gt=0)):
    
    # pesquisa criada automaticamente com status_id = 0
    survey_model = Survey(**survey_request.model_dump(), survey_status_id = survey_status_id)
    db.add(survey_model)
    db.commit()


@router.delete("/delete/{survey_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_survey(db: db_dependency, survey_id: int = Path(gt=0)):
    
    survey_model = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if survey_model is None: raise HTTPException(status_code=404, detail="Survey not found.")
    
    db.query(Survey).filter(Survey.survey_id == survey_id).first().delete()
    db.commit()
