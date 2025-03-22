import os
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["OPNEAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")

mcp = FastMCP("Math")
tavily = TavilyClient()

@mcp.tool()
def add(a: int, b: int) -> int:
    return a-b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    return a*b

@mcp.tool()
def search_web(query: str):
    """Searches the web for Best Results"""
    response = tavily.search(query)
    return str(response)


@mcp.tool()
def write_report(query: str, content):
    """Write a report on retrieved search results
    Args
    query: Query to write about
    content: search result retrieved from search_web function
    """
    prompt = query + "\ncontent: " + content
    response = llm.invoke(prompt)
    return response




if __name__ == "__main__":
    print("Server Starting ...")
    mcp.run(transport="stdio")