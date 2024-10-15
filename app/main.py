import multiprocessing
import os
import logging
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Depends, Request, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from app import models
from app.db import SessionLocal, engine, Base
from auth import router as auth_router
from chatbot import start_chatbot
from dotenv import load_dotenv
from app.neo4j_db import Neo4jConnection

# 加载环境变量
load_dotenv()

# 日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global neo4j_db
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    neo4j_db = Neo4jConnection(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    logger.info("Neo4j 连接已建立")

    yield

    if neo4j_db is not None:
        neo4j_db.close()
        logger.info("Neo4j 连接已关闭")
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)
neo4j_db = None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_user(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db), user: str = Cookie(None)):
    if not user:
        return RedirectResponse(url="/login")

    user_info = load_user(user, db)
    return templates.TemplateResponse("index.html", {"request": request, "nav_class": "home", "user": user_info})

@app.get("/kg", response_class=HTMLResponse)
async def kg_page(request: Request, db: Session = Depends(get_db), user: str = Cookie(None)):
    user_info = load_user(user, db) if user else None
    return templates.TemplateResponse("kg.html", {"request": request, "nav_class": "kg", "user": user_info})

@app.get("/kgqa", response_class=HTMLResponse)
async def kgqa_page(request: Request, db: Session = Depends(get_db), user: str = Cookie(None)):
    user_info = load_user(user, db) if user else None
    return templates.TemplateResponse("kgqa.html", {"request": request, "nav_class": "kgqa", "user": user_info})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

if __name__ == "__main__":
    # 启动 gradio
    gradio_process = multiprocessing.Process(target=start_chatbot)
    gradio_process.start()

    # 启动 fastapi
    fastapi_process = multiprocessing.Process(target=run_fastapi)
    fastapi_process.start()

    try:
        gradio_process.join()
        fastapi_process.join()
    except KeyboardInterrupt:
        print("正在退出...")
        gradio_process.terminate()
        fastapi_process.terminate()
        gradio_process.join()
        fastapi_process.join()
        print("退出成功。")