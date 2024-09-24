import logging
from typing import List
from langchain_core.messages import HumanMessage, SystemMessage
import gradio as gr
from langchain_community.chat_models import ChatZhipuAI
from dotenv import load_dotenv
import os

from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
load_dotenv()

logger = logging.getLogger(__name__)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有关核桃的农业问答助手。"
               "请你利用所学知识生成准确科学的答案。"
               "请尽量将答案解释的简洁易懂，避免长篇大论。"
               "你的用户对象主要是农民，需要科学但又易懂的指导。"),
])

model = ChatZhipuAI(name='glm-4-flash', prompt_template=prompt)

async def chat_bot(question: str, history: List[List[str]]):
    logger.info(f"收到问题: {question}")
    system_message = SystemMessage(content=prompt.format())
    human_message = HumanMessage(content=question)
    inputs = [system_message, human_message]
    result = ''
    async for r in model.astream(inputs):
        content = r.content
        result += content
        yield result

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