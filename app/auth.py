from fastapi import APIRouter, Depends, Request, Response, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
import bcrypt
from starlette.templating import Jinja2Templates

from app import models
from app.db import SessionLocal

templates = Jinja2Templates(directory="templates")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def load_user(username: str, db: Session):
    return db.query(models.User).filter(models.User.username == username).first()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/auth/token")
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

@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key="user", path="/")

    return RedirectResponse(url='/login', status_code=303)

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post('/register')
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