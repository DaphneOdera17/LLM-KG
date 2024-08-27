# LLM-KG

在根目录下运行

```python
py manage.py runserver 8000
```

本机网页 127.0.0.1:8000



## Docker 运行 （依赖未完整， 完善系统再测试）

在项目根目录

### 构建 Docker 镜像

```shell
docker build -t kgllm .
```

### 运行 Docker 容器

```shell
docker run -p 8000:8000 kgllm
```

