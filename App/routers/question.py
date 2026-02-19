from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import Question, QuestionDependency, QuestionType, QuestionOption, Survey


router = APIRouter(
    prefix='/question',
    tags=['question']
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


class QuestionTypeRequest(BaseModel):
    question_type: str = Field(min_length=5)


class QuestionRequest(BaseModel):
    order: int = Field(min=1)
    question_text: str = Field(min_length=5)
    is_mandatory: bool = Field(default=False)
    is_independent: bool = Field(default=True)


class QuestionOptionRequest(BaseModel):
    order: int = Field(min=1)
    value: str = Field(min_length=3)


class QuestionDependencyRequest(BaseModel):
    source_question_option_id: int = Field(ge=1)
    target_question_id: int = Field(ge=1)


### ENDPOINTS ###

@router.get("/question-type", status_code=status.HTTP_200_OK)
async def get_all_question_types(db: db_dependency):
    return db.query(QuestionType).all()


@router.post("/question-type/create", status_code=status.HTTP_201_CREATED)
async def create_question_type(db: db_dependency, question_type_request: QuestionTypeRequest):
    
    question_type_model = QuestionType(**question_type_request.model_dump())
    db.add(question_type_model)
    db.commit()


@router.delete("/question-type/delete/{question_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question_type(db: db_dependency, question_type_id: int = Path(gt=0)):

    question_type_model = db.query(QuestionType).filter(QuestionType.question_type_id == question_type_id).first()
    if question_type_model is None: raise HTTPException(status_code=404, detail="Question type not found.")

    db.query(QuestionType).filter(QuestionType.question_type_id == question_type_id).first().delete()
    db.commit()


@router.get("/{survey_id}", status_code=status.HTTP_200_OK)
async def get_all_question(db: db_dependency, survey_id: int = Path(gt=0)):

    survey_model = db.query(Survey).filter(Survey.survey_id == survey_id).first()
    if survey_model is None: raise HTTPException(status_code=404, detail="Survey not found.")

    return db.query(Question).filter(Question.survey_id == survey_id).all()


@router.post("/create/{survey_id}", status_code=status.HTTP_201_CREATED)
async def create_question(db: db_dependency, question_request: QuestionRequest,
                          survey_id: int = Path(gt=0)):
    
    question_model = Question(**question_request.model_dump(),
                              survey_id=survey_id, question_type_id=1)
    db.add(question_model)
    db.commit()


class UpdateQuestionRequest(BaseModel):
    order: Optional[int] = Field(default=None, ge=1)
    question_text: Optional[str] = Field(default=None, min_length=5)
    is_mandatory: Optional[bool] = Field(default=None)
    is_independent: Optional[bool] = Field(default=None)


@router.put("/update/{question_id}", status_code=status.HTTP_200_OK)
async def update_question(db: db_dependency, question_request: UpdateQuestionRequest,
                          question_id: int = Path(gt=0)):
    
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found.")

    if question_request.order is not None:
        question.order = question_request.order
    if question_request.question_text is not None:
        question.question_text = question_request.question_text
    if question_request.is_mandatory is not None:
        question.is_mandatory = question_request.is_mandatory
    if question_request.is_independent is not None:
        question.is_independent = question_request.is_independent

    db.commit()
    db.refresh(question)
    
    survey_id_json = {
        "survey_id": question.survey_id
    }

    return survey_id_json


@router.delete("/delete/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(db: db_dependency, question_id: int = Path(gt=0)):
    
    question_model = db.query(Question).filter(Question.question_id == question_id).first()
    if question_model is None: raise HTTPException(status_code=404, detail="Question not found.")
    
    db.query(Question).filter(Question.question_id == question_id).delete()
    db.commit()


@router.get("/question-option/{question_id}", status_code=status.HTTP_200_OK)
async def get_all_question_options(db: db_dependency, question_id: int = Path(gt=0)):
    
    question_model = db.query(Question).filter(Question.question_id == question_id).first()
    if question_model is None: raise HTTPException(status_code=404, detail="Question not found.")
    
    return db.query(QuestionOption).filter(QuestionOption.question_id == question_id).all()


@router.post("/question_option/create/{question_id}", status_code=status.HTTP_201_CREATED)
async def create_question_option(db: db_dependency, question_option_request: QuestionOptionRequest,
                          question_id: int = Path(gt=0)):
    
    question_option_model = QuestionOption(**question_option_request.model_dump(),
                              question_id=question_id)
    db.add(question_option_model)
    db.commit()


@router.delete("/question_option/delete/{question_option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question_option(db: db_dependency, question_option_id: int = Path(gt=0)):
    
    question_option_model = db.query(QuestionOption).filter(QuestionOption.question_option_id == question_option_id).first()
    if question_option_model is None: raise HTTPException(status_code=404, detail="Question option not found.")
    
    db.query(QuestionOption).filter(QuestionOption.question_option_id == question_option_id).delete()
    db.commit()


@router.post("/dependency/{question_id}/create", status_code=status.HTTP_201_CREATED)
async def create_dependency(db: db_dependency, question_dependency_request: QuestionDependencyRequest,
                            question_id: int = Path(gt=0)):
    
    question_model = db.query(Question).filter(Question.question_id == question_id).first()
    if question_model is None: raise HTTPException(status_code=404, detail="Question not found.")
    
    question_dependency_model = QuestionDependency(
        src_question_id=question_id,
        src_question_option_id=question_dependency_request.source_question_option_id,
        target_question_id=question_dependency_request.target_question_id,
        survey_id=question_model.survey_id
    )
    
    db.add(question_dependency_model)
    db.commit()
    
    return {"order": question_model.order}

@router.delete("/dependency/{question_id}/delete", status_code=status.HTTP_201_CREATED)
async def create_dependency(db: db_dependency, question_id: int = Path(gt=0)):
    
    question_model = db.query(Question).filter(Question.question_id == question_id).first()
    if question_model is None: raise HTTPException(status_code=404, detail="Question not found.")
    
    db.query(QuestionDependency).filter((QuestionDependency.src_question_id == question_id) | 
                                       (QuestionDependency.target_question_id == question_id) ).delete()
    db.commit()