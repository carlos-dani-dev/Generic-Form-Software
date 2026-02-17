from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status
from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import Question, QuestionOption, Survey, SurveyStatus
from .auth import get_current_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/admin',
    tags=['admin']
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
user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="App/templates")


def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


### PAGES ###

@router.get("/survey")
async def render_survey_page(request: Request, db: db_dependency):
    try:
        access_token = request.cookies.get('access_token')
        user = await get_current_user(access_token)

        if user is None:
            return redirect_to_login()
        
        surveys = db.query(Survey).all()
        
        return templates.TemplateResponse("survey-page.html", {"request": request, "surveys": surveys, "user": user})
    except:
        return redirect_to_login()


@router.get("/question/{survey_id}")
async def render_question_page(request: Request, db: db_dependency, survey_id: int = Path(gt=0)):
    try:
        access_token = request.cookies.get('access_token')
        user = await get_current_user(access_token)
        
        if user is None:
            return redirect_to_login()
        
        questions = db.query(Question).filter(Question.survey_id == survey_id).order_by(Question.order).all()
        
        return templates.TemplateResponse("question-page.html", {"request": request, "questions": questions, "user": user})
    except:
        return redirect_to_login()


@router.get("/edit-question/{question_id}")
async def render_question_page(request: Request, db: db_dependency, question_id: int = Path(gt=0)):
    try:
        access_token = request.cookies.get('access_token')
        user = await get_current_user(access_token)

        if user is None:
            return redirect_to_login()
        
        question = db.query(Question).filter(Question.question_id == question_id).first()
        
        question_options = db.query(QuestionOption).filter(QuestionOption.question_id == question_id).all()

        return templates.TemplateResponse("edit-question-page.html", {"request": request, "question": question, "question_options": question_options, "user": user})
    except:
        return redirect_to_login()


@router.get("/create-survey")
async def render_create_survey_page(request: Request, db: db_dependency):
    try:
        access_token = request.cookies.get('access_token')
        user = await get_current_user(access_token)

        if user is None:
            return redirect_to_login()
        
        surveys_status = db.query(SurveyStatus).all()
        
        return templates.TemplateResponse("create-survey-page.html", {"request": request, "surveys_status": surveys_status})
    except:
        return redirect_to_login()


@router.get("/create-question/{survey_id}")
async def render_create_question_page(request: Request, db: db_dependency, survey_id: int):
    try:
        access_token = request.cookies.get('access_token')
        user = await get_current_user(access_token)

        if user is None:
            return redirect_to_login()
        
        surveys_status = db.query(SurveyStatus).all()
        
        return templates.TemplateResponse("create-question-page.html", {"request": request})
    except:
        return redirect_to_login()

### ENDPOINTS ###