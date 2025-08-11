# https://github.com/agentika/agentize/blob/main/examples/mcp_chatbot.py
import os

import chainlit as cl
import google.generativeai as genai
from agentize.utils import configure_langfuse
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger


def configure_gemini():
    """配置 Gemini API"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("請在 .env 檔案中設定 GEMINI_API_KEY")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')


class GeminiAgent:
    def __init__(self) -> None:
        load_dotenv(find_dotenv(), override=True)
        configure_langfuse()
        self.model = configure_gemini()
        self.messages = []

    async def connect(self) -> None:
        logger.info("Gemini model ready")

    async def cleanup(self) -> None:
        logger.info("Gemini cleanup completed")

    async def run(self, message: str) -> str:
        try:
            # 使用 Gemini 直接生成回應
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return f"抱歉，我遇到了一個錯誤：{str(e)}"


@cl.on_app_startup
async def connect() -> None:
    await gemini_agent.connect()


@cl.on_app_shutdown
async def cleanup() -> None:
    await gemini_agent.cleanup()


@cl.on_message
async def chat(message: cl.Message) -> None:
    content = await gemini_agent.run(message.content)
    await cl.Message(content=content).send()

# main
gemini_agent = GeminiAgent()
