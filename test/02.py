from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

# 环境变量
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["ZHIPUAI_API_KEY"] = "8b4fa95036a9d5a9f7a9ad2156b36e5f.ePH8ShMykmW3Obqk"

model_name = "glm-4-flash"


# 1. Create prompt template
# prompt_template = ChatPromptTemplate.from_messages([("system", "把用户提出的问题用{language}代码实现，"
#                                                                "直接写代码，不要出现任何说明和其他文字"
#                                                                "不要有任何注释，不要写多余的示例，"
#                                                                "封装成函数即可，不需要在主函数运行，"
#                                                                "变量名尽量用单字母代替，保持抽象和简洁，"
#                                                                "例如left写成l，right写成r"
#                                                                "代码保持高度抽象和简洁，要求行数尽可能少："),
#                                                     ("user", "{text}")])

prompt_template = ChatPromptTemplate.from_messages([("system", "把用户提出的问题用{language}代码实现，"
                                                               "直接写代码，不要出现任何说明和其他文字"
                                                               "不要有任何注释，不要写多余的示例，"
                                                               "封装成函数即可，不需要在主函数运行，"
                                                               "变量名尽量用单字母代替，保持抽象和简洁，"
                                                               "例如left写成l，right写成r"
                                                               "代码保持高度抽象和简洁，要求行数尽可能少："),
                                                    ("user", "{text}")])


# 2. Create model
model = ChatZhipuAI(model=model_name)

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt_template | model | parser


# 4. App definition
app = FastAPI(title="LangChain Server",
              version="1.0",
              description="A simple API server using LangChain's Runnable interfaces")

# 5. Adding chain route
add_routes(app,chain,path="/chain",)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)