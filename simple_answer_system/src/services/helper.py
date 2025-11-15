from dotenv import load_dotenv
import os
# from langchain.agents import create_react_agent
from langgraph.prebuilt import create_react_agent
from langchain_openai import AzureChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import AsyncIterator, Iterable
import json
import asyncio

def prompt(user_input: str) -> str:
    return f"""
Context:
You are a personal assistant called Aurora, who helps gives details and answers about a simple news api which you have access to, use the methods to answer the query.

User question: {user_input}
"""

async def create_agent():
    load_dotenv()
    endpoint = os.environ.get("AZURE_OPENAI_API_ENDPOINT")
    deployment = os.environ.get("DEPLOYMENT")
    subscription_key = os.environ.get("SUBSCRIPTION_KEY")
    api_version = os.environ.get("API_VERSION")

    azure_llm = AzureChatOpenAI(
        azure_deployment=deployment,
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
        streaming=False,
    )

    client = MultiServerMCPClient(
        {
            "SimpleAnsweringSystemMCP": {
                "transport": "streamable_http",
                "url": f"{os.environ.get('ALLOWED_MCP_ORIGINS')}/mcp",
            }
        }
    )

    tools = await client.get_tools()
    agent = create_react_agent(azure_llm, tools)
    return agent

def _chunk_text(text: str, n: int = 6) -> Iterable[str]:
    """Simple chunker to simulate token-like streaming."""
    for i in range(0, len(text), n):
        yield text[i : i + n]

async def _sse_stream_text(final_text: str) -> AsyncIterator[str]:
    """SSE stream that only sends the final assistant message, chunked."""
    yield "event: start\ndata: {}\n\n"
    for piece in _chunk_text(final_text):
        yield f"event: token\ndata: {json.dumps({'delta': piece})}\n\n"
        await asyncio.sleep(0.1)
    yield f"event: end\ndata: {json.dumps({'text': final_text})}\n\n"

def _extract_final_text(run_result) -> str:
    """
    LangGraph `create_react_agent` returns a dict-like state; the final
    assistant output is in the last message.
    """
    messages = run_result.get("messages", [])
    if not messages:
        return ""
    last = messages[-1]
    content = getattr(last, "content", "")
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content)