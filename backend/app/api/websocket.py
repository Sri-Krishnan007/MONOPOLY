"""
Indian Monopoly (KUBER) - WebSocket Real-Time Game Handler
"""
import asyncio
import time
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Any

from app.engine.room_manager import room_manager
from app.engine.game_engine import KuberGameEngine
from app.engine.ai_bot import AITycoonEngine
from app.models.game_state import TurnPhase

ws_router = APIRouter()

@ws_router.websocket("/ws/{room_id}/{player_id}")
async def game_websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    await room_manager.connect_socket(room_id, player_id, websocket)
    game = room_manager.get_room(room_id)
    if not game:
        await websocket.close(code=1008, reason="Room does not exist")
        return

    # Broadcast initial state
    await room_manager.broadcast_state(room_id)

    try:
        while True:
            data = await websocket.receive_json()
            action_type = data.get("type")
            payload = data.get("payload", {})

            # 1. Start Game
            if action_type == "START_GAME":
                if game.host_id == player_id:
                    KuberGameEngine.start_game(game)
                    await room_manager.broadcast_state(room_id)
                    await trigger_ai_if_needed(room_id)

            # 2. Add AI Bot
            elif action_type == "ADD_BOT":
                if game.host_id == player_id:
                    room_manager.add_bot_to_room(room_id)
                    await room_manager.broadcast_state(room_id)

            # 3. Roll Dice
            elif action_type == "ROLL_DICE":
                KuberGameEngine.roll_dice(game, player_id)
                await room_manager.broadcast_state(room_id)
                await trigger_ai_if_needed(room_id)

            # 4. Buy Property
            elif action_type == "BUY_PROPERTY":
                space_id = payload.get("space_id")
                if space_id is not None:
                    KuberGameEngine.buy_property(game, player_id, space_id)
                    await room_manager.broadcast_state(room_id)
                    await trigger_ai_if_needed(room_id)

            # 5. Decline & Auction
            elif action_type == "DECLINE_BUY":
                space_id = payload.get("space_id")
                if space_id is not None:
                    KuberGameEngine.decline_to_buy_and_auction(game, player_id, space_id)
                    await room_manager.broadcast_state(room_id)
                    await trigger_ai_if_needed(room_id)

            # 6. Place Auction Bid
            elif action_type == "PLACE_BID":
                amount = payload.get("amount", 0)
                KuberGameEngine.place_bid(game, player_id, amount)
                await room_manager.broadcast_state(room_id)

            # 7. Conclude Auction
            elif action_type == "CONCLUDE_AUCTION":
                KuberGameEngine.conclude_auction(game)
                await room_manager.broadcast_state(room_id)
                await trigger_ai_if_needed(room_id)

            # 8. Construction: Build Bhavan
            elif action_type == "BUILD_BHAVAN":
                space_id = payload.get("space_id")
                if space_id is not None:
                    KuberGameEngine.build_bhavan(game, player_id, space_id)
                    await room_manager.broadcast_state(room_id)

            # 9. Construction: Build Mahal
            elif action_type == "BUILD_MAHAL":
                space_id = payload.get("space_id")
                if space_id is not None:
                    KuberGameEngine.build_mahal(game, player_id, space_id)
                    await room_manager.broadcast_state(room_id)

            # 10. Mortgage / Unmortgage
            elif action_type == "MORTGAGE_PROPERTY":
                space_id = payload.get("space_id")
                if space_id is not None:
                    KuberGameEngine.mortgage_property(game, player_id, space_id)
                    await room_manager.broadcast_state(room_id)

            elif action_type == "UNMORTGAGE_PROPERTY":
                space_id = payload.get("space_id")
                if space_id is not None:
                    KuberGameEngine.unmortgage_property(game, player_id, space_id)
                    await room_manager.broadcast_state(room_id)

            # 11. Jail Bail / Card
            elif action_type == "PAY_JAIL_BAIL":
                KuberGameEngine.pay_jail_bail(game, player_id)
                await room_manager.broadcast_state(room_id)

            elif action_type == "USE_JAIL_CARD":
                KuberGameEngine.use_jail_card(game, player_id)
                await room_manager.broadcast_state(room_id)

            # 12. End Turn
            elif action_type == "END_TURN":
                KuberGameEngine.end_turn(game, player_id)
                await room_manager.broadcast_state(room_id)
                await trigger_ai_if_needed(room_id)

    except WebSocketDisconnect:
        room_manager.disconnect_socket(room_id, player_id)
        await room_manager.broadcast_state(room_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        room_manager.disconnect_socket(room_id, player_id)

async def trigger_ai_if_needed(room_id: str):
    """If current player is an AI bot, execute steps automatically with natural delays."""
    game = room_manager.get_room(room_id)
    if not game or game.status != "playing":
        return

    cur = game.current_player
    if not cur or not cur.is_bot or cur.is_bankrupt:
        return

    # Run AI bot loop asynchronously
    asyncio.create_task(run_ai_turn_async(room_id))

async def run_ai_turn_async(room_id: str):
    game = room_manager.get_room(room_id)
    if not game or game.status != "playing":
        return

    cur = game.current_player
    if not cur or not cur.is_bot or cur.is_bankrupt:
        return

    # Small delay for realistic feeling
    await asyncio.sleep(1.2)
    
    # 1. Roll or Jail Action
    if game.turn_phase in [TurnPhase.PRE_ROLL, TurnPhase.IN_JAIL_DECISION]:
        AITycoonEngine.process_ai_turn(game)
        await room_manager.broadcast_state(room_id)
        await asyncio.sleep(1.2)

    # 2. If decision needed (Buy or Auction)
    if game.turn_phase == TurnPhase.BUY_OR_AUCTION_DECISION:
        AITycoonEngine.process_ai_turn(game)
        await room_manager.broadcast_state(room_id)
        await asyncio.sleep(1.0)

    # 3. If in Post-Turn (build & end turn)
    if game.turn_phase == TurnPhase.POST_TURN:
        AITycoonEngine.process_ai_turn(game)
        await room_manager.broadcast_state(room_id)
        
        # Check next player if also AI
        await asyncio.sleep(0.8)
        await trigger_ai_if_needed(room_id)
