import chainlit as cl
from llama_index.llms.openai import OpenAI
from main import create_agent

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = OpenAI(model="gpt-4o-mini", streaming=True)  # Enable streaming

@cl.on_chat_start
async def start():
    await cl.Message(content="Hello! How can I help you?").send()

@cl.on_message
async def main(message: cl.Message):
    try:
        msg = cl.Message(content="")  # Initialize an empty message
        
        # Properly awaiting the async generator before looping
        response = await llm.astream_complete(message.content)

        async for chunk in response:
            text = chunk.delta # extract new text
            if text:  
                await msg.stream_token(text)  # Stream
        await msg.send()

    except Exception as e:
        await cl.Message(content=f"Error: {e}", author="Assistant").send()