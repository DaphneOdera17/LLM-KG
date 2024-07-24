# 使用基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 将代码文件夹复制到工作目录
COPY ../../tempCode/example-project/code .

# 安装项目依赖项
RUN pip install -r requests.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 暴露应用程序的端口
EXPOSE 8000

# 定义启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
