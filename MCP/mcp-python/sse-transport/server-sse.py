import os
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
import uvicorn
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient

from dotenv import load_dotenv
load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["OPNEAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

mcp = FastMCP("example-server")
sse = SseServerTransport("/messages")

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

async def handle_sse(scope, receive, send):
    async with sse.connect_sse(scope, receive, send) as streams:
        await mcp.run(streams[0], streams[1], mcp.create_initialization_options())

async def handle_messages(scope, receive, send):
    await sse.handle_post_message(scope, receive, send)

starlette_app = Starlette(
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"]),
    ]
)


if __name__ == "__main__":
    uvicorn.run(starlette_app, host="0.0.0.0", port=8000)
