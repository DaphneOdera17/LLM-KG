import os

# API Keys
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["ZHIPUAI_API_KEY"] = "8b4fa95036a9d5a9f7a9ad2156b36e5f.ePH8ShMykmW3Obqk"

# 导入模型
from langchain_community.chat_models import ChatZhipuAI

model = ChatZhipuAI(name='glm-4-flash')

# 历史对话
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory

# 存储所有对话内容
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# 提示
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([("system", "你是一个有关{species}的农业问答助手。"
                                                      "请你利用所学知识生成准确科学的答案。"
                                                      "请尽量将答案解释的简洁易懂，避免长篇大论。"
                                                      "你的用户对象主要是农民，需要科学但又易懂的指导。"),
                                           MessagesPlaceholder(variable_name="messages"), ])

# 裁剪器
from langchain_core.messages import trim_messages

trimmer = trim_messages(max_tokens=1000000,
                        strategy="last",
                        token_counter=model,
                        include_system=True,
                        allow_partial=False,
                        start_on="human")

# 拼接裁剪器
from operator import itemgetter
from langchain_core.runnables import RunnablePassthrough

trimmer = RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer)

# 定义链
chain = trimmer | prompt | model

# 给链加入历史消息功能
from langchain_core.runnables.history import RunnableWithMessageHistory

bot = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="messages")

# 对话id
config = {"configurable": {"session_id": "abc1"}}

# 输入/输出
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# 前端集成
import gradio as gr

def chatbot_interface(question: str, species : str):
    inputs = {"messages": [HumanMessage(content=question)],
              "species": species}
    result = ''
    for r in bot.stream(inputs, config=config):
        result += r.content
        yield result

# 创建 Gradio 界面
interface = gr.Interface(fn=chatbot_interface,  # 处理输入的函数
                         inputs=[gr.Textbox(label="植物"), gr.Textbox(label="问题")],  # 输入类型为文本框
                         outputs="markdown",  # 输出类型为文本框
                         title="农业问答助手",  # 标题
                         description="你可以问任何与农业相关的问题。")  # 描述

if __name__ == "__main__":
    interface.launch(share=True)

    # while True:
    #     content = input()
    #     if content == "exit":
    #         break
    #
    #     inputs = {"messages": [HumanMessage(content=content)],
    #          "species": "核桃"}
    #
    #     for r in bot.stream(inputs, config=config):
    #         print(r.content, end='')
