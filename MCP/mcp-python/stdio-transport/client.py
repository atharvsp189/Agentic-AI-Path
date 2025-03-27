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
    args=["server.py"],
)


system_prompt = "You are a helpful Research Assistant with access to set of tools. You are given a query and you need to search it about that over the internet and need to write a detailed report about that."

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            print("Inside Client Session")
            await session.initialize()
            print("Session Initialized")
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)
            
            print("Agent Started Ask Queries...")
            query = input("Query: ")

            agent_response = await agent.ainvoke(
                {"messages": [ 
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": query} 
                ]}
            )
            


            agent_response = await agent.ainvoke(
                {"messages": query}
            )

            print("Agent Response: ")
            print(agent_response["content"])
            

if __name__ == '__main__':
    print("Inside Main")
    result = asyncio.run(run_agent())