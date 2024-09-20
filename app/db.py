from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 连接数据库，用户名 root 密码 root 数据表名 kgllm
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/kgllm?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()