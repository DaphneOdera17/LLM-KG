FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
