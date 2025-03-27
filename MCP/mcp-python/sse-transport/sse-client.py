import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

from dotenv import load_dotenv
load_dotenv()
os.environ["OPNEAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o")

async def connect_server():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            print("Session Initialized")
        
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            query = input("Enter Query: ")
            agent_response = await agent.ainvoke(
                {"messages": query}
            )
            return agent_response["messages"]

if __name__ == '__main__':
    print("Agent Started...")
    asyncio.run(connect_server())
    