from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from simple_answer_system.src.routes import routes

app = FastAPI()
load_dotenv()

origins = [
    os.environ.get("ALLOWED_MCP_ORIGINS")
]

app.include_router(routes.router)

@app.get("/")
async def root():
    return {"message": "Simple Answer System is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.environ.get("SERVER_HOST"), port=int(os.environ.get("SERVER_PORT")))