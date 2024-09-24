设置项目的根目录为 LLM-KG 而不是 app 下，否则需手动修改 app/main.py 下的 static 和 templates 文件路径等

## 安装项目依赖

在项目根目录下

建议先创建 conda 虚拟环境后再进行：

```shell
pip install -r requirements.txt
pip install pymysql
pip install httpx_sse
pip install pyjwt
```

## 项目配置
根目录下创建 .env

里面配置 api 等:

智谱 ai
```
LANGCHAIN_TRACING_V2=
LANGCHAIN_API_KEY=
ZHIPUAI_API_KEY=
```

## 项目详情
登录注册逻辑位于 app/auth.py

问答界面逻辑位于 app/chatbot.py

## 项目启动

### 方式一

在根目录下

```shell
python -m app.main
```

### 方式二

进入 app 目录 main.py 文件，运行 

## 网页

网页链接  http://127.0.0.1:8000 