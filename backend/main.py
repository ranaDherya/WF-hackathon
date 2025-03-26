from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat_routes import router as chat_router

from contextlib import asynccontextmanager
from Core.chatbot import MyChatBot
from Core.utility import getApiKey
from typing import Dict, Any


@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialize the Client and add it to app.state
    '''
    getApiKey()
    app.state.chatbot = MyChatBot()
    yield
    ''' Run on shutdown
        Close the connection
        Clear variables and release the resources
    '''

app = FastAPI(lifespan=lifespan)


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome!!!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
