import json
import multiprocessing
import uvicorn
from fastapi import FastAPI, Depends, Request, Response, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import bcrypt
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import gradio as gr
from app import models
from app.db import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/auth/token")
async def login(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = load_user(username, db)
    if user is None or not verify_password(password, user.password):
        return JSONResponse(status_code=400, content={'error': '用户名或密码错误！'})

    response = JSONResponse(content={'redirect': '/', 'message': '登录成功！'})
    response.set_cookie(key="user", value=user.username)

    return response


@app.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="user", path="/")

    return RedirectResponse(url='/login', status_code=303)


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post('/register')
async def register(
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        db: Session = Depends(get_db)
):
    if not username or not password or not email:
        return JSONResponse(status_code=400, content={'error': '所有字段都是必填的！'})

    existing_user = db.query(models.User).filter(models.User.username == username).first()
    if existing_user:
        return JSONResponse(status_code=400, content={'error': '用户名已存在！'})

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    new_user = models.User(username=username, password=hashed_password.decode('utf-8'), email=email)
    db.add(new_user)
    db.commit()

    return JSONResponse(content={'redirect': '/login/', 'message': '注册成功！'})


def load_user(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@app.get("/kg", response_class=HTMLResponse)
async def kg_page(request: Request, db: Session = Depends(get_db), user: str = Cookie(None)):
    user_info = load_user(user, db) if user else None
    return templates.TemplateResponse("kg.html", {"request": request, "nav_class": "kg", "user": user_info})


@app.get("/kgqa", response_class=HTMLResponse)
async def kgqa_page(request: Request, db: Session = Depends(get_db), user: str = Cookie(None)):
    user_info = load_user(user, db) if user else None
    return templates.TemplateResponse("kgqa.html", {"request": request, "nav_class": "kgqa", "user": user_info})


def chat_bot(message, history):
    history = [[y, x] for x, y in history]
    data = {
        'query': message,
        'history': history
    }
    data = json.dumps(data)
    return "Response from chatbot"


def start_chatbot():
    gr.ChatInterface(
        fn=chat_bot,
        chatbot=gr.Chatbot(height=500, value=[["你好", "您好，我是核桃助手，我将尽力帮助您解决问题。"]]),
        theme="soft",
        examples=["核桃是什么", "核桃2", "核桃3"],
        retry_btn=None,
        submit_btn="发送",
        undo_btn="删除前言",
        clear_btn="清空",
    ).queue().launch(server_name="127.0.0.1", server_port=7860, share=True, inbrowser=False)


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

    gradio_process.join()
    fastapi_process.join()
