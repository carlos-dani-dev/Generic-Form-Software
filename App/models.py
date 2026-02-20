from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)


class Survey(Base):
    __tablename__ = "survey"
    
    survey_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    survey_status_id = Column(Integer, ForeignKey("survey_status.survey_status_id"))
    
    survey_status = relationship("SurveyStatus")
    
class SurveyStatus(Base):
    __tablename__ = "survey_status"
    
    survey_status_id = Column(Integer, primary_key=True, index=True)
    survey_status = Column(String, unique=True, nullable=False)

class Response(Base):
    __tablename__ = "response"
    
    response_id = Column(Integer, primary_key=True, index=True)
    begin_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    survey_id = Column(Integer, ForeignKey("survey.survey_id"), nullable=True)
    city_id = Column(Integer, ForeignKey("city.city_id"), nullable=False)

    survey = relationship("Survey")
    city = relationship("City")

class Answer(Base):
    __tablename__ = "answer"
        
    answer_id = Column(Integer, primary_key=True, index=True)
    answer = Column(String, nullable=True)
    response_id = Column(Integer, ForeignKey("response.response_id"), nullable=True)
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=True)
    
    response = relationship("Response")
    question = relationship("Question")

class Question(Base):
    __tablename__ = "question"
    
    __table_args__ = (
        UniqueConstraint("order", "survey_id", name="uq_question_order_survey"),
    )
    
    question_id = Column(Integer, primary_key=True, index=True)
    order = Column(Integer, nullable=False)
    question_text = Column(String, nullable=False)
    is_mandatory = Column(Boolean, nullable=False)
    is_independent = Column(Boolean, nullable=False)
    
    question_type_id = Column(Integer, ForeignKey("question_type.question_type_id"))
    survey_id = Column(Integer, ForeignKey("survey.survey_id"), nullable=False)
    
    question_type = relationship("QuestionType")
    survey = relationship("Survey")

class AnswerOption(Base):
    __tablename__ = "answer_option"
    
    answer_option_id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey("answer.answer_id"))
    question_option_id = Column(Integer, ForeignKey("question_option.question_option_id"), nullable=False)
    
    question_option = relationship("QuestionOption")

class QuestionOption(Base):
    __tablename__ = "question_option"
    
    question_option_id = Column(Integer, primary_key=True)
    order = Column(Integer, nullable=False)
    value = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    
    question = relationship("Question")

class QuestionType(Base):
    __tablename__ = "question_type"
    
    question_type_id = Column(Integer, primary_key=True)
    question_type = Column(String, nullable=False, unique=True)
    
class City(Base):
    __tablename__ = "city"
    
    city_id = Column(Integer, primary_key=True)
    city_name = Column(String, nullable=False)

class QuestionDependency(Base):
    __tablename__ = "question_dependency"
    
    question_dependency_id = Column(Integer, primary_key=True)
    
    src_question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    src_question_option_id = Column(Integer,
        ForeignKey("question_option.question_option_id"), nullable=False)
    target_question_id = Column(Integer, ForeignKey("question.question_id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("survey.survey_id"), nullable=False)