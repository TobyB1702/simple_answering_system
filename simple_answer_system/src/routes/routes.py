from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from simple_answer_system.src.services.helper import prompt, create_agent, _sse_stream_text, _extract_final_text
import asyncio

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/ask")
async def ask(query: str):
    """
    Runs the agent to completion (so it can use tools and reason),
    then streams ONLY the final assistant message back via SSE.
    """
    agent = await create_agent()

    #run_result = await agent.ainvoke({"messages": [("human", prompt(query))]})
    run_result = await agent.ainvoke({"messages": [("human", prompt(query))]})

    final_text = _extract_final_text(run_result)

    async def generator():
        try:
            async for evt in _sse_stream_text(final_text):
                yield evt
        except (asyncio.CancelledError, ConnectionResetError):
                return

    return StreamingResponse(generator(), media_type="text/event-stream")