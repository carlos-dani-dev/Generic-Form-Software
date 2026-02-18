from .routers import admin, answer, auth, question, response, survey, city
from fastapi import FastAPI
from .database import engine, Base
from . import models

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(answer.router)
app.include_router(question.router)
app.include_router(response.router)
app.include_router(survey.router)
app.include_router(city.router)


@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    templates = Jinja2Templates(directory="App/templates")
    app.mount("/static", StaticFiles(directory="App/static"), name="static")