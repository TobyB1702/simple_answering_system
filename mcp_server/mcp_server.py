from typing import Any
from loguru import logger
from mcp.server.fastmcp import FastMCP
import requests
from dotenv import load_dotenv
import os

load_dotenv()
query_api = os.environ.get("QUERY_API")

# Initialize FastMCP server
mcp = FastMCP("SimpleAnsweringSystemMCP")


@mcp.tool()
def get_movies(skip: int, limit: int, query: str) -> Any:
    """
    Fetch news movies based on the provided query.
    """
    logger.info(f"Fetching news articles for topic: {query}")

    url = f"{query_api}/movies/"
    payload = {
    "skip": skip,
    "limit": limit,
    "query": query
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()

@mcp.tool()
def get_messages(skip: int, limit) -> Any:
    """
    Fetch news messages based on the provided query.
    """

    url = f"{query_api}/messages/"
    payload = {
    "skip": skip,
    "limit": limit,
    }

    response = requests.get(url, params=payload)
    response.raise_for_status()

    return response.json()

@mcp.tool()
def get_random_image() -> Any:
    """
    Fetch random 
    """

    url = f"{query_api}/image/"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()

if __name__ == "__main__":
    mcp.settings.host = os.environ.get("MCP_SERVER_HOST")
    mcp.settings.port = int(os.environ.get("MCP_SERVER_PORT"))
    mcp.run(transport="streamable-http")

    
