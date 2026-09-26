"""
Indian Monopoly (KUBER) - REST API Routes
"""
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from app.models.board_data import BOARD_SPACES, ColorGroup, COLOR_GROUPS_MAP
from app.models.cards_data import CHANCE_CARDS, COMMUNITY_CARDS
from app.models.game_state import PlayerToken, PLAYER_TOKENS_INFO
from app.engine.room_manager import room_manager
from app.engine.game_engine import KuberGameEngine

router = APIRouter()

class CreateRoomRequest(BaseModel):
    host_name: str
    token: str = PlayerToken.AUTO_RICKSHAW

class JoinRoomRequest(BaseModel):
    room_code: str
    player_name: str
    token: str = PlayerToken.ROYAL_ELEPHANT

@router.get("/board")
def get_board_layout():
    """Returns static board data with all 40 spaces, descriptions, and color groups."""
    return {
        "spaces": [s.model_dump() for s in BOARD_SPACES],
        "color_groups": COLOR_GROUPS_MAP,
        "tokens": PLAYER_TOKENS_INFO
    }

@router.get("/cards")
def get_cards_catalog():
    """Returns catalog of all Chance and Community Chest cards."""
    return {
        "chance": [c.model_dump() for c in CHANCE_CARDS],
        "community": [c.model_dump() for c in COMMUNITY_CARDS]
    }

@router.post("/rooms/create")
def create_room(req: CreateRoomRequest):
    game = room_manager.create_room(
        host_name=req.host_name,
        host_token=req.token
    )
    return {
        "room_id": game.room_id,
        "room_code": game.room_code,
        "host_id": game.host_id,
        "game": game.model_dump()
    }

@router.post("/rooms/join")
def join_room(req: JoinRoomRequest):
    game = room_manager.find_room_by_code(req.room_code)
    if not game:
        raise HTTPException(status_code=404, detail="Room code not found")
    if game.status != "lobby":
        raise HTTPException(status_code=400, detail="Game has already started")
    if len(game.players) >= 8:
        raise HTTPException(status_code=400, detail="Room is full (max 8 players)")

    # Check if token is already taken
    token = req.token
    used_tokens = [p.token for p in game.players]
    if token in used_tokens:
        for t in PLAYER_TOKENS_INFO:
            if t["id"] not in used_tokens:
                token = t["id"]
                break

    player_id = str(uuid.uuid4())
    success = KuberGameEngine.add_player(
        game=game,
        player_id=player_id,
        name=req.player_name,
        token=token
    )
    if not success:
        raise HTTPException(status_code=400, detail="Could not join room")

    return {
        "room_id": game.room_id,
        "room_code": game.room_code,
        "player_id": player_id,
        "game": game.model_dump()
    }

@router.get("/rooms/{room_id}")
def get_room_state(room_id: str):
    game = room_manager.get_room(room_id)
    if not game:
        raise HTTPException(status_code=404, detail="Room not found")
    return game.model_dump()
