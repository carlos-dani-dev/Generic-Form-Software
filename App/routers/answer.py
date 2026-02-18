from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Request, status

from ..database import SessionLocal
from pydantic import BaseModel, Field
from ..models import Question, Answer, Response, AnswerOption, QuestionOption


router = APIRouter(
    prefix='/answer',
    tags=['answer']
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


class AnswerRequest(BaseModel):
    answer: Optional[str] = None


class AnswerVariousRequest(BaseModel):
    answer: Optional[str] = None
    question_id: int = Field(min=1)


class AnswerAndAnswerOptionRequest(BaseModel):
    answer: AnswerVariousRequest
    question_option_id: int


class AnswerListRequest(BaseModel):
    answers: list[AnswerAndAnswerOptionRequest]


### PAGES ###

### ENDPOINTS ###

@router.get("/by_question/{question_id}", status_code=status.HTTP_200_OK)
async def get_all_answer_by_question(db: db_dependency, question_id: int = Path(gt=0)):
    
    question_model = db.query(Question).filter(Question.question_id == question_id).first()
    if question_model is None: raise HTTPException(status_code=404, detail="Question not found.")
    
    answer_model = db.query(Answer).filter(Answer.question_id == question_id).all()
    
    return answer_model


@router.get("/by_response/{response_id}", status_code=status.HTTP_200_OK)
async def get_all_answer_by_response(db: db_dependency, response_id: int = Path(gt=0)):
    
    response_model = db.query(Response).filter(Response.response_id == response_id).first()
    if response_model is None: raise HTTPException(status_code=404, detail="Response not found.")
    
    answer_model = db.query(Answer).filter(Answer.response_id == response_id).all()
    
    return answer_model


@router.post("/create/only_one/{response_id}/{question_id}", status_code=status.HTTP_201_CREATED)
async def create_answer(db: db_dependency, answer_request: AnswerRequest, response_id: int = Path(gt=0), question_id: int = Path(gt=0)):

    response_model = db.query(Response).filter(Response.response_id == response_id).first()
    if response_model is None: raise HTTPException(status_code=404, detail="Response not found.")

    question_model = db.query(Question).filter(Question.question_id == question_id).first()
    if question_model is None: raise HTTPException(status_code=404, detail="Question not found.")
    
    answer_model = Answer(**answer_request.model_dump(), response_id=response_id, question_id=question_id)
    
    db.add(answer_model)
    db.commit()
    db.refresh(answer_model)
    
    return {"answer_id": answer_model.answer_id}


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_answers_and_answer_options(request: Request, db: db_dependency,
        answer_list_request: AnswerListRequest):

    response_id = request

    response_model = db.query(Response).filter(Response.response_id == response_id).first()
    if response_model is None: raise HTTPException(status_code=404, detail="Response not found.")

    for answer in answer_list_request.answers:
        answer_model = Answer(**answer.answer.model_dump(),
                        response_id=response_id)
        db.add(answer_model)
        db.flush()
    
        answer_option_model = AnswerOption(answer_id=answer_model.answer_id,
                                           question_option_id=answer.question_option_id)
        db.add(answer_option_model)

    db.commit()
    db.refresh(answer_model)


@router.delete("/delete/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(db: db_dependency, answer_id: int = Path(gt=0)):
    
    answer_model = db.query(Answer).filter(Answer.answer_id == answer_id).first()
    if answer_model is None: raise HTTPException(status_code=404, detail="Answer not found.")
    
    db.query(Answer).filter(Answer.answer_id == answer_id).first().delete()
    db.commit()


@router.get("/answer_option/by_answer/{answer_id}", status_code=status.HTTP_200_OK)
async def get_all_answer_option_by_answer(db: db_dependency, answer_id: int = Path(gt=0)):
    
    answer_model = db.query(Answer).filter(Answer.answer_id == answer_id).first()
    if answer_model is None: raise HTTPException(status_code=404, detail="Answer not found.")
    
    answer_option_model = db.query(AnswerOption).filter(AnswerOption.answer_id == answer_id).all()
    
    return answer_option_model


@router.get("/answer_option/by_question_option/{question_option_id}", status_code=status.HTTP_200_OK)
async def get_all_answer_option_by_question_option(db: db_dependency, question_option_id: int = Path(gt=0)):
    
    question_option_model = db.query(QuestionOption).filter(QuestionOption.question_option_id == question_option_id).first()
    if question_option_model is None: raise HTTPException(status_code=404, detail="Question option not found.")
    
    answer_option_model = db.query(AnswerOption).filter(AnswerOption.question_option_id == question_option_id).all()
    
    return answer_option_model


@router.post("/answer_option/create/{answer_id}/{question_option_id}", status_code=status.HTTP_201_CREATED)
async def create_answer_option(db: db_dependency, answer_id: int = Path(gt=0), question_option_id: int = Path(gt=0)):

    answer_model = db.query(Answer).filter(Answer.answer_id == answer_id).first()
    if answer_model is None: raise HTTPException(status_code=404, detail="Answer not found.")

    question_option_model = db.query(QuestionOption).filter(QuestionOption.question_option_id == question_option_id).first()
    if question_option_model is None: raise HTTPException(status_code=404, detail="Question option not found.")

    answer_option_model = AnswerOption(answer_id=answer_id, question_option_id=question_option_id)

    db.add(answer_option_model)
    db.commit()
    db.refresh(answer_option_model)


@router.delete("/answer_option/delete/{answer_option_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer_option(db: db_dependency, answer_option_id: int = Path(gt=0)):

    answer_option_model = db.query(AnswerOption).filter(AnswerOption.answer_option_id == answer_option_id).first()
    if answer_option_model is None: raise HTTPException(status_code=404, detail="Answer option not found.")

    db.query(AnswerOption).filter(AnswerOption.answer_option_id == answer_option_id).first().delete()
    db.commit()
