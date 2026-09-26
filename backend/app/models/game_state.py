"""
Indian Monopoly (KUBER) - Complete Game State and Action Pydantic Models
"""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
import time

class PlayerToken:
    AUTO_RICKSHAW = "auto_rickshaw"
    ROYAL_ELEPHANT = "royal_elephant"
    CRICKET_BAT = "cricket_bat"
    CUTTING_CHAI = "cutting_chai"
    LOCOMOTIVE = "locomotive"
    SCOOTER = "scooter"
    LOTUS = "lotus"
    CLAPPERBOARD = "clapperboard"

PLAYER_TOKENS_INFO = [
    {"id": PlayerToken.AUTO_RICKSHAW, "name": "Auto-Rickshaw", "hindi": "ऑटो-रिक्शा", "finish": "Antique Brass", "icon": "truck"},
    {"id": PlayerToken.ROYAL_ELEPHANT, "name": "Royal Elephant", "hindi": "शाही हाथी", "finish": "Rose Copper", "icon": "shield"},
    {"id": PlayerToken.CRICKET_BAT, "name": "Cricket Bat & Ball", "hindi": "बल्ला और गेंद", "finish": "Sterling Silver", "icon": "trophy"},
    {"id": PlayerToken.CUTTING_CHAI, "name": "Cutting Chai", "hindi": "कटिंग चाय", "finish": "Stainless Steel", "icon": "coffee"},
    {"id": PlayerToken.LOCOMOTIVE, "name": "WAP-7 Engine", "hindi": "रेल इंजन", "finish": "Gunmetal", "icon": "train"},
    {"id": PlayerToken.SCOOTER, "name": "Bajaj Chetak", "hindi": "चेतक स्कूटर", "finish": "Matte Nickel", "icon": "bike"},
    {"id": PlayerToken.LOTUS, "name": "National Lotus", "hindi": "कमल पुष्प", "finish": "24K Gold", "icon": "flower"},
    {"id": PlayerToken.CLAPPERBOARD, "name": "Bollywood Reel", "hindi": "सिनेमा क्लैपर", "finish": "Black Chrome", "icon": "film"}
]

class Player(BaseModel):
    id: str
    name: str
    token: str = PlayerToken.AUTO_RICKSHAW
    color: str = "#E65100"
    cash: int = 15000
    position: int = 0
    in_jail: bool = False
    jail_turns: int = 0
    get_out_of_jail_cards: int = 0
    is_bankrupt: bool = False
    is_bot: bool = False
    bot_profile: Optional[str] = None
    connected: bool = True
    last_active: float = Field(default_factory=time.time)

class PropertyOwnership(BaseModel):
    space_id: int
    owner_id: str
    bhavans: int = 0  # 0 to 4
    has_mahal: bool = False
    is_mortgaged: bool = False

class TurnPhase:
    PRE_ROLL = "pre_roll"
    ROLLED = "rolled"
    BUY_OR_AUCTION_DECISION = "buy_or_auction_decision"
    AUCTION_IN_PROGRESS = "auction_in_progress"
    CARD_DRAWN = "card_drawn"
    IN_JAIL_DECISION = "in_jail_decision"
    PAY_RENT_DUE = "pay_rent_due"
    POST_TURN = "post_turn"
    GAME_OVER = "game_over"

class AuctionState(BaseModel):
    space_id: int
    current_bid: int = 100
    highest_bidder_id: Optional[str] = None
    active_bidders: List[str] = []
    round: int = 1
    started_at: float = Field(default_factory=time.time)
    expires_at: float = 0.0

class TradeOffer(BaseModel):
    trade_id: str
    from_player_id: str
    to_player_id: str
    offered_cash: int = 0
    requested_cash: int = 0
    offered_properties: List[int] = []
    requested_properties: List[int] = []
    offered_jail_cards: int = 0
    requested_jail_cards: int = 0
    status: str = "pending"  # "pending", "accepted", "declined", "cancelled"

class GameLog(BaseModel):
    id: str
    timestamp: float = Field(default_factory=time.time)
    message: str
    hindi_message: Optional[str] = None
    player_id: Optional[str] = None
    log_type: str = "info"  # "info", "cash", "property", "dice", "card", "jail", "alert"

class GameState(BaseModel):
    room_id: str
    room_code: str
    host_id: str
    status: str = "lobby"  # "lobby", "playing", "completed"
    players: List[Player] = []
    current_player_index: int = 0
    dice_1: int = 1
    dice_2: int = 1
    doubles_count: int = 0
    turn_phase: str = TurnPhase.PRE_ROLL
    properties: Dict[int, PropertyOwnership] = {}
    kismat_deck: List[str] = []  # card IDs
    panchayat_deck: List[str] = []
    bank_bhavans: int = 32
    bank_mahals: int = 12
    logs: List[GameLog] = []
    active_auction: Optional[AuctionState] = None
    active_trade: Optional[TradeOffer] = None
    last_drawn_card: Optional[Dict[str, Any]] = None
    winner_id: Optional[str] = None
    created_at: float = Field(default_factory=time.time)
    turn_number: int = 1

    @property
    def current_player(self) -> Optional[Player]:
        if 0 <= self.current_player_index < len(self.players):
            return self.players[self.current_player_index]
        return None
