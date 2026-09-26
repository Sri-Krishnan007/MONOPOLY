"""
Indian Monopoly (KUBER) - FastAPI Application Server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as api_router
from app.api.websocket import ws_router

app = FastAPI(
    title="KUBER - The Great Indian Property Empire Backend",
    description="FastAPI WebSocket & REST game engine for the Indian Monopoly property-trading board game.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
app.include_router(ws_router)

@app.get("/")
def root():
    return {
        "game": "KUBER: The Great Indian Property Empire",
        "status": "Online",
        "version": "1.0.0",
        "endpoints": {
            "api_board": "/api/board",
            "api_cards": "/api/cards",
            "create_room": "/api/rooms/create",
            "join_room": "/api/rooms/join",
            "ws_game": "/ws/{room_id}/{player_id}"
        }
    }
