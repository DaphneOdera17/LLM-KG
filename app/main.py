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
from auth import router as auth_router

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router)

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


# 示例回答字典
responses = {
    "核桃是什么": "核桃是一种坚果，富含营养，对人体健康有益。",
    "核桃有哪些病虫害": "核桃常见的病虫害包括核桃炭疽病、核桃黑斑病、核桃象鼻虫等。",
    "核桃适合在什么环境种植": "核桃适合在温暖湿润的气候条件下种植，土壤要求排水良好，富含有机质。"
}


def chat_bot(message, history):
    history = [[y, x] for x, y in history]
    data = {
        'query': message,
        'history': history
    }
    data = json.dumps(data)

    # 查找回答
    response = responses.get(message, "抱歉，我不太明白您的问题。")
    return response


def start_chatbot():
    gr.ChatInterface(
        fn=chat_bot,
        chatbot=gr.Chatbot(height=500, value=[["你好", "您好，我是核桃小助手，我将尽力帮助您解决问题。"]]),
        theme="soft",
        title="核桃小助手",
        examples=["核桃是什么", "核桃有哪些病虫害", "核桃适合在什么环境种植?"],
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