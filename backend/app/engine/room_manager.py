"""
Indian Monopoly (KUBER) - Room and Session Manager
"""
import uuid
import random
import string
import time
from typing import Dict, Optional, List
from fastapi import WebSocket

from app.models.game_state import GameState, PlayerToken
from app.engine.game_engine import KuberGameEngine
from app.engine.ai_bot import AI_PROFILES

class RoomManager:
    def __init__(self):
        self.rooms: Dict[str, GameState] = {}
        self.connections: Dict[str, Dict[str, WebSocket]] = {}  # room_id -> {player_id: WebSocket}

    def generate_room_code(self) -> str:
        chars = string.ascii_uppercase + string.digits
        while True:
            code = "KUBER-" + "".join(random.choices(chars, k=4))
            if not any(r.room_code == code for r in self.rooms.values()):
                return code

    def create_room(self, host_name: str, host_token: str = PlayerToken.AUTO_RICKSHAW) -> GameState:
        room_id = str(uuid.uuid4())
        room_code = self.generate_room_code()
        host_id = str(uuid.uuid4())
        
        game = KuberGameEngine.create_game(
            room_id=room_id,
            room_code=room_code,
            host_id=host_id,
            host_name=host_name,
            host_token=host_token
        )
        self.rooms[room_id] = game
        self.connections[room_id] = {}
        return game

    def get_room(self, room_id: str) -> Optional[GameState]:
        return self.rooms.get(room_id)

    def find_room_by_code(self, room_code: str) -> Optional[GameState]:
        clean_code = room_code.strip().upper()
        for room in self.rooms.values():
            if room.room_code.upper() == clean_code:
                return room
        return None

    def add_bot_to_room(self, room_id: str) -> Optional[str]:
        game = self.get_room(room_id)
        if not game or game.status != "lobby" or len(game.players) >= 8:
            return None

        # Pick an unused bot profile
        used_names = [p.name for p in game.players]
        bot_profile = next((b for b in AI_PROFILES if b["name"] not in used_names), None)
        if not bot_profile:
            bot_profile = {
                "name": f"AI Tycoon #{len(game.players) + 1}",
                "token": PlayerToken.SCOOTER,
                "style": "growth",
                "description": "Smart algorithmic investor."
            }

        bot_id = f"bot-{uuid.uuid4()}"
        KuberGameEngine.add_player(
            game=game,
            player_id=bot_id,
            name=bot_profile["name"],
            token=bot_profile["token"],
            is_bot=True,
            bot_profile=bot_profile["name"]
        )
        return bot_id

    async def connect_socket(self, room_id: str, player_id: str, websocket: WebSocket):
        await websocket.accept()
        if room_id not in self.connections:
            self.connections[room_id] = {}
        self.connections[room_id][player_id] = websocket
        
        # Mark player connected
        game = self.get_room(room_id)
        if game:
            p = next((p for p in game.players if p.id == player_id), None)
            if p:
                p.connected = True

    def disconnect_socket(self, room_id: str, player_id: str):
        if room_id in self.connections and player_id in self.connections[room_id]:
            del self.connections[room_id][player_id]
        game = self.get_room(room_id)
        if game:
            p = next((p for p in game.players if p.id == player_id), None)
            if p:
                p.connected = False

    async def broadcast_state(self, room_id: str):
        game = self.get_room(room_id)
        if not game or room_id not in self.connections:
            return

        payload = {
            "type": "GAME_STATE_UPDATE",
            "game": game.model_dump()
        }

        dead_sockets = []
        for pid, ws in self.connections[room_id].items():
            try:
                await ws.send_json(payload)
            except Exception:
                dead_sockets.append(pid)

        for pid in dead_sockets:
            self.disconnect_socket(room_id, pid)

room_manager = RoomManager()
