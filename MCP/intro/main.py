import os
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from bs4 import BeautifulSoup
import os 


from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

mcp = FastMCP('intro')
tavily = TavilyClient()

@mcp.tool()
def search_web(query: str):
    """
    This toold searches the web for a query
    Args:
        query: The query to search the web for
    Returns:
        A Dictionary with response from the web
    """
    response = tavily.search(query=query, max_results=3)
    print(response)
    return response

@mcp.tool()
def add(a: int, b: int):
    """
    This tools adds two numbers
    Args:
        a: The first number
        b: The second number
    Returns:
        The sum of the two numbers
    """
    return f"The sum of {a} and {b} is {a - b}"

@mcp.tool()
def myName():
    """
    This tool returns my name
    """
    return "My name is Atharv" 


if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run(transport='stdio')

