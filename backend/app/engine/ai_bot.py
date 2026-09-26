"""
Indian Monopoly (KUBER) - AI Tycoon Bot Decision Engine
"""
import random
import time
from typing import Dict, Any, Optional
from app.models.board_data import (
    BOARD_SPACES, COLOR_GROUPS_MAP, SpaceType, get_space_by_id
)
from app.models.game_state import GameState, Player, TurnPhase
from app.engine.game_engine import KuberGameEngine

AI_PROFILES = [
    {
        "name": "Mukesh Bhai (Billionaire)",
        "token": "royal_elephant",
        "style": "aggressive",
        "description": "High-capital conglomerate builder. Dominates utilities, green & blue properties."
    },
    {
        "name": "Rakesh Ji (Dalal Street Bull)",
        "token": "auto_rickshaw",
        "style": "trader",
        "description": "Savvy value investor. Rapidly completes sets and loves high-yield orange/red belts."
    },
    {
        "name": "Tech Founder (Bengaluru)",
        "token": "cricket_bat",
        "style": "growth",
        "description": "Aggressive scaling mindset. Builds Bhavans early and fast."
    },
    {
        "name": "Chaiwala Tycoon",
        "token": "cutting_chai",
        "style": "defensive",
        "description": "Patient, cash-flow oriented master of railways and early low-cost monopolies."
    }
]

class AITycoonEngine:
    @staticmethod
    def process_ai_turn(game: GameState) -> Optional[Dict[str, Any]]:
        cur = game.current_player
        if not cur or not cur.is_bot or cur.is_bankrupt:
            return None

        # 1. In Jail Decision
        if cur.in_jail:
            if cur.get_out_of_jail_cards > 0:
                KuberGameEngine.use_jail_card(game, cur.id)
            elif cur.cash > 3000:
                KuberGameEngine.pay_jail_bail(game, cur.id)
            # Roll dice (whether in jail or released)
            return KuberGameEngine.roll_dice(game, cur.id)

        # 2. Pre-Roll Phase
        if game.turn_phase == TurnPhase.PRE_ROLL:
            return KuberGameEngine.roll_dice(game, cur.id)

        # 3. Buy or Auction Decision
        elif game.turn_phase == TurnPhase.BUY_OR_AUCTION_DECISION:
            space = get_space_by_id(cur.position)
            if space:
                # Keep ₹1,000 cash safety buffer
                if cur.cash >= (space.price + 1000):
                    return KuberGameEngine.buy_property(game, cur.id, space.id)
                elif cur.cash >= space.price and space.type in [SpaceType.TRANSPORT, SpaceType.UTILITY]:
                    return KuberGameEngine.buy_property(game, cur.id, space.id)
                else:
                    return KuberGameEngine.decline_to_buy_and_auction(game, cur.id, space.id)
            return KuberGameEngine.end_turn(game, cur.id)

        # 4. Auction in Progress (AI bidding)
        elif game.turn_phase == TurnPhase.AUCTION_IN_PROGRESS and game.active_auction:
            space = get_space_by_id(game.active_auction.space_id)
            current_bid = game.active_auction.current_bid
            max_bid_willing = int(space.price * 1.15) if space else 1000

            # If current highest bidder is already this bot, don't outbid itself
            if game.active_auction.highest_bidder_id != cur.id:
                next_bid = current_bid + 200
                if next_bid <= max_bid_willing and cur.cash >= (next_bid + 1000):
                    return KuberGameEngine.place_bid(game, cur.id, next_bid)

        # 5. Post Turn Phase (Construction & End Turn)
        elif game.turn_phase == TurnPhase.POST_TURN:
            # Check if bot can build Bhavans/Mahals
            AITycoonEngine._try_ai_construction(game, cur)
            return KuberGameEngine.end_turn(game, cur.id)

        return None

    @staticmethod
    def _try_ai_construction(game: GameState, player: Player):
        if player.cash < 3000:
            return

        # Scan for monopolies
        for color, spaces in COLOR_GROUPS_MAP.items():
            owns_all = all(
                game.properties.get(sid) and game.properties[sid].owner_id == player.id and not game.properties[sid].is_mortgaged
                for sid in spaces
            )
            if owns_all:
                for sid in spaces:
                    space = get_space_by_id(sid)
                    own = game.properties.get(sid)
                    if not space or not own:
                        continue
                    # Upgrade to Mahal
                    if own.bhavans == 4 and not own.has_mahal and player.cash >= (space.hotel_cost + 2000):
                        KuberGameEngine.build_mahal(game, player.id, sid)
                    # Build Bhavan
                    elif own.bhavans < 4 and not own.has_mahal and player.cash >= (space.house_cost + 2000):
                        KuberGameEngine.build_bhavan(game, player.id, sid)
