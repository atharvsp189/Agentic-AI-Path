from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio

import os
from dotenv import load_dotenv
load_dotenv()
os.environ["OPNEAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o")

server_params = StdioServerParameters(
    command="python",
    args=["server.py"]
)


async def run_agent(query: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            agent_response = await agent.ainvoke(
                {"messages": query}
            )
            return agent_response["messages"]

if __name__ == '__main__':
    print("Inside Main")
    print("Agent Started Ask Queries...")
    query = input("Query: ")
    result = asyncio.run(run_agent(query))
    print("Result : ")
    print(result)