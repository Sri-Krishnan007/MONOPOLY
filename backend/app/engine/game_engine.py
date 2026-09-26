"""
Indian Monopoly (KUBER) - Core Game Engine
Handles all game rules, dice rolls, movement, rent calculation, auctions, trades, construction, and bankruptcy.
"""
import random
import time
import uuid
from typing import Dict, List, Optional, Tuple, Any

from app.models.board_data import (
    BOARD_SPACES, COLOR_GROUPS_MAP, TRANSPORT_SPACES, UTILITY_SPACES,
    SpaceType, ColorGroup, get_space_by_id, BoardSpace
)
from app.models.cards_data import (
    KISMAT_CARDS, PANCHAYAT_CARDS, CardActionType, GameCard
)
from app.models.game_state import (
    GameState, Player, PropertyOwnership, TurnPhase, AuctionState,
    TradeOffer, GameLog
)

class KuberGameEngine:
    @staticmethod
    def create_game(room_id: str, room_code: str, host_id: str, host_name: str, host_token: str) -> GameState:
        # Shuffle card decks
        kismat_ids = [c.id for c in KISMAT_CARDS]
        panchayat_ids = [c.id for c in PANCHAYAT_CARDS]
        random.shuffle(kismat_ids)
        random.shuffle(panchayat_ids)

        host_player = Player(
            id=host_id,
            name=host_name,
            token=host_token,
            color="#E65100",
            cash=15000,
            position=0
        )

        game = GameState(
            room_id=room_id,
            room_code=room_code,
            host_id=host_id,
            status="lobby",
            players=[host_player],
            current_player_index=0,
            properties={},
            kismat_deck=kismat_ids,
            panchayat_deck=panchayat_ids,
            bank_bhavans=32,
            bank_mahals=12,
            logs=[
                GameLog(
                    id=str(uuid.uuid4()),
                    message=f"Game lobby created by {host_name}.",
                    hindi_message=f"{host_name} द्वारा खेल लॉबी बनाई गई।"
                )
            ]
        )
        return game

    @staticmethod
    def add_player(game: GameState, player_id: str, name: str, token: str, is_bot: bool = False, bot_profile: Optional[str] = None) -> bool:
        if game.status != "lobby" or len(game.players) >= 8:
            return False
        
        # Color palette for players
        player_colors = ["#E65100", "#1A237E", "#1B5E20", "#B71C1C", "#4A148C", "#006064", "#F57F17", "#3E2723"]
        color = player_colors[len(game.players) % len(player_colors)]

        player = Player(
            id=player_id,
            name=name,
            token=token,
            color=color,
            cash=15000,
            position=0,
            is_bot=is_bot,
            bot_profile=bot_profile
        )
        game.players.append(player)
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{name} joined the empire!",
            hindi_message=f"{name} खेल में शामिल हुए!",
            player_id=player_id
        ))
        return True

    @staticmethod
    def start_game(game: GameState) -> bool:
        if len(game.players) < 2:
            return False
        game.status = "playing"
        game.turn_phase = TurnPhase.PRE_ROLL
        game.current_player_index = 0
        game.turn_number = 1
        
        cur = game.current_player
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"Game started! {cur.name}'s turn to roll.",
            hindi_message=f"खेल शुरू! {cur.name} की पासा फेंकने की बारी है।"
        ))
        return True

    @staticmethod
    def roll_dice(game: GameState, player_id: str) -> Dict[str, Any]:
        cur = game.current_player
        if not cur or cur.id != player_id or cur.is_bankrupt:
            return {"error": "Not your turn"}
        
        if game.turn_phase not in [TurnPhase.PRE_ROLL, TurnPhase.IN_JAIL_DECISION]:
            return {"error": "Cannot roll dice at this phase"}

        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        game.dice_1 = d1
        game.dice_2 = d2
        is_doubles = (d1 == d2)
        total_roll = d1 + d2

        log_msg = f"{cur.name} rolled {d1} and {d2} (Total: {total_roll})."
        if is_doubles:
            log_msg += " Doubles!"
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=log_msg,
            player_id=player_id,
            log_type="dice"
        ))

        # Handle In-Jail Roll
        if cur.in_jail:
            if is_doubles:
                cur.in_jail = False
                cur.jail_turns = 0
                game.doubles_count = 0
                game.logs.append(GameLog(
                    id=str(uuid.uuid4()),
                    message=f"{cur.name} rolled doubles and is released from Police Chowki!",
                    hindi_message=f"{cur.name} ने जोड़ा पासा फेंककर हवालात से रिहाई पाई!",
                    player_id=player_id,
                    log_type="jail"
                ))
                return KuberGameEngine._advance_player(game, cur, total_roll)
            else:
                cur.jail_turns += 1
                if cur.jail_turns >= 3:
                    # Must pay fine of ₹500 and move
                    if cur.cash >= 500:
                        cur.cash -= 500
                        cur.in_jail = False
                        cur.jail_turns = 0
                        game.logs.append(GameLog(
                            id=str(uuid.uuid4()),
                            message=f"{cur.name} spent 3 turns in detention. Paid ₹500 fine and was released.",
                            player_id=player_id,
                            log_type="jail"
                        ))
                        return KuberGameEngine._advance_player(game, cur, total_roll)
                    else:
                        # Need to mortgage or go bankrupt
                        game.turn_phase = TurnPhase.POST_TURN
                        return {"action": "must_raise_funds_for_jail"}
                else:
                    game.logs.append(GameLog(
                        id=str(uuid.uuid4()),
                        message=f"{cur.name} did not roll doubles. Remains in Police Chowki ({cur.jail_turns}/3 turns).",
                        player_id=player_id,
                        log_type="jail"
                    ))
                    game.turn_phase = TurnPhase.POST_TURN
                    return {"action": "stayed_in_jail"}

        # Normal roll doubles check
        if is_doubles:
            game.doubles_count += 1
            if game.doubles_count >= 3:
                # 3 consecutive doubles -> Go to Jail!
                cur.in_jail = True
                cur.position = 10
                cur.jail_turns = 0
                game.doubles_count = 0
                game.turn_phase = TurnPhase.POST_TURN
                game.logs.append(GameLog(
                    id=str(uuid.uuid4()),
                    message=f"{cur.name} rolled 3 consecutive doubles! Sent directly to Police Chowki for speeding!",
                    hindi_message=f"{cur.name} ने लगातार 3 बार जोड़े पासे फेंके! तेज़ रफ़्तार के लिए हवालात भेजे गए!",
                    player_id=player_id,
                    log_type="jail"
                ))
                return {"action": "sent_to_jail_speeding"}
        else:
            game.doubles_count = 0

        return KuberGameEngine._advance_player(game, cur, total_roll)

    @staticmethod
    def _advance_player(game: GameState, player: Player, steps: int) -> Dict[str, Any]:
        old_pos = player.position
        new_pos = (old_pos + steps) % 40
        player.position = new_pos

        # Check passing Aarambh (GO)
        if new_pos < old_pos and steps > 0 and old_pos != 0:
            player.cash += 2000
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"{player.name} passed Aarambh (GO) and collected ₹2,000 salary!",
                hindi_message=f"{player.name} ने आरम्भ पार किया और ₹2,000 वेतन प्राप्त किया!",
                player_id=player.id,
                log_type="cash"
            ))

        space = get_space_by_id(new_pos)
        if not space:
            game.turn_phase = TurnPhase.POST_TURN
            return {"action": "moved"}

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} landed on {space.name} ({space.hindi_name}).",
            player_id=player.id,
            log_type="info"
        ))

        return KuberGameEngine._resolve_landed_space(game, player, space)

    @staticmethod
    def _resolve_landed_space(game: GameState, player: Player, space: BoardSpace) -> Dict[str, Any]:
        # 1. Aarambh (GO)
        if space.type == SpaceType.GO:
            player.cash += 2000
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"{player.name} landed right on Aarambh (GO) and received ₹2,000 bonus!",
                player_id=player.id,
                log_type="cash"
            ))
            game.turn_phase = TurnPhase.POST_TURN
            return {"action": "landed_go"}

        # 2. Go to Police Chowki (Pos 30)
        elif space.type == SpaceType.GO_TO_JAIL:
            player.in_jail = True
            player.position = 10
            player.jail_turns = 0
            game.doubles_count = 0
            game.turn_phase = TurnPhase.POST_TURN
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"{player.name} received a Court Summons and was escorted to Police Chowki!",
                hindi_message=f"{player.name} को न्यायालय समन मिला और हवालात भेज दिया गया!",
                player_id=player.id,
                log_type="jail"
            ))
            return {"action": "go_to_jail"}

        # 3. Police Chowki visiting / Free Parking
        elif space.type in [SpaceType.JAIL, SpaceType.FREE_PARKING]:
            game.turn_phase = TurnPhase.POST_TURN
            return {"action": "safe_space"}

        # 4. Tax Spaces (Aaykar & Luxury GST Cess)
        elif space.type == SpaceType.TAX:
            tax_amount = space.price  # 2000 or 1000
            player.cash -= tax_amount
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"{player.name} paid ₹{tax_amount:,} for {space.name}.",
                player_id=player.id,
                log_type="cash"
            ))
            KuberGameEngine._check_bankruptcy(game, player)
            game.turn_phase = TurnPhase.POST_TURN
            return {"action": "paid_tax", "amount": tax_amount}

        # 5. Kismat & Panchayat Decks
        elif space.type in [SpaceType.KISMAT, SpaceType.PANCHAYAT]:
            return KuberGameEngine._draw_card(game, player, space.type)

        # 6. Purchasable Real Estate (Property, Transport, Utility)
        elif space.type in [SpaceType.PROPERTY, SpaceType.TRANSPORT, SpaceType.UTILITY]:
            ownership = game.properties.get(space.id)
            if not ownership:
                # Unowned -> Offer Buy or Auction
                game.turn_phase = TurnPhase.BUY_OR_AUCTION_DECISION
                return {"action": "buy_or_auction", "space_id": space.id, "price": space.price}
            elif ownership.owner_id == player.id:
                # Own property -> Nothing to pay
                game.turn_phase = TurnPhase.POST_TURN
                return {"action": "own_property"}
            elif ownership.is_mortgaged:
                game.logs.append(GameLog(
                    id=str(uuid.uuid4()),
                    message=f"{space.name} is mortgaged. No rent is due.",
                    player_id=player.id
                ))
                game.turn_phase = TurnPhase.POST_TURN
                return {"action": "mortgaged_rent_free"}
            else:
                # Pay Rent to Owner
                owner = next((p for p in game.players if p.id == ownership.owner_id), None)
                if not owner or owner.is_bankrupt:
                    game.turn_phase = TurnPhase.POST_TURN
                    return {"action": "owner_inactive"}

                rent_due = KuberGameEngine.calculate_rent(game, space.id, game.dice_1 + game.dice_2)
                player.cash -= rent_due
                owner.cash += rent_due
                game.logs.append(GameLog(
                    id=str(uuid.uuid4()),
                    message=f"{player.name} paid ₹{rent_due:,} rent to {owner.name} for {space.name}.",
                    hindi_message=f"{player.name} ने {owner.name} को ₹{rent_due:,} किराया दिया।",
                    player_id=player.id,
                    log_type="cash"
                ))
                KuberGameEngine._check_bankruptcy(game, player, creditor=owner)
                game.turn_phase = TurnPhase.POST_TURN
                return {"action": "paid_rent", "rent": rent_due, "owner_name": owner.name}

        game.turn_phase = TurnPhase.POST_TURN
        return {"action": "resolved"}

    @staticmethod
    def calculate_rent(game: GameState, space_id: int, dice_sum: int = 7) -> int:
        space = get_space_by_id(space_id)
        ownership = game.properties.get(space_id)
        if not space or not ownership or ownership.is_mortgaged:
            return 0

        # Transport Hub Rent
        if space.type == SpaceType.TRANSPORT:
            owned_transports = sum(
                1 for tid in TRANSPORT_SPACES
                if game.properties.get(tid) and game.properties[tid].owner_id == ownership.owner_id and not game.properties[tid].is_mortgaged
            )
            # 1=250, 2=500, 3=1000, 4=2000
            rent_map = {1: 250, 2: 500, 3: 1000, 4: 2000}
            return rent_map.get(owned_transports, 250)

        # Public Utility Rent
        elif space.type == SpaceType.UTILITY:
            owned_utilities = sum(
                1 for uid in UTILITY_SPACES
                if game.properties.get(uid) and game.properties[uid].owner_id == ownership.owner_id and not game.properties[uid].is_mortgaged
            )
            multiplier = 100 if owned_utilities >= 2 else 40
            return multiplier * dice_sum

        # Standard Color Property Rent
        elif space.type == SpaceType.PROPERTY:
            if ownership.has_mahal:
                return space.rent_hotel
            elif ownership.bhavans == 4:
                return space.rent_4_house
            elif ownership.bhavans == 3:
                return space.rent_3_house
            elif ownership.bhavans == 2:
                return space.rent_2_house
            elif ownership.bhavans == 1:
                return space.rent_1_house
            else:
                # Check Monopoly
                color = space.color_group
                group_spaces = COLOR_GROUPS_MAP.get(color, [])
                is_monopoly = all(
                    game.properties.get(sid) and game.properties[sid].owner_id == ownership.owner_id
                    for sid in group_spaces
                )
                return (space.base_rent * 2) if is_monopoly else space.base_rent

        return 0

    @staticmethod
    def buy_property(game: GameState, player_id: str, space_id: int) -> Dict[str, Any]:
        cur = game.current_player
        if not cur or cur.id != player_id:
            return {"error": "Not your turn"}
        if game.turn_phase != TurnPhase.BUY_OR_AUCTION_DECISION or cur.position != space_id:
            return {"error": "Invalid property purchase action"}
        
        space = get_space_by_id(space_id)
        if not space or space.id in game.properties:
            return {"error": "Property unavailable"}

        if cur.cash < space.price:
            return {"error": "Insufficient funds to buy property"}

        cur.cash -= space.price
        game.properties[space_id] = PropertyOwnership(
            space_id=space_id,
            owner_id=player_id
        )
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{cur.name} bought {space.name} ({space.hindi_name}) for ₹{space.price:,}!",
            hindi_message=f"{cur.name} ने ₹{space.price:,} में {space.hindi_name} खरीदा!",
            player_id=player_id,
            log_type="property"
        ))
        game.turn_phase = TurnPhase.POST_TURN
        return {"status": "purchased", "space_id": space_id}

    @staticmethod
    def decline_to_buy_and_auction(game: GameState, player_id: str, space_id: int) -> Dict[str, Any]:
        cur = game.current_player
        if not cur or cur.id != player_id:
            return {"error": "Not your turn"}
        
        space = get_space_by_id(space_id)
        if not space or space.id in game.properties:
            return {"error": "Invalid property for auction"}

        active_player_ids = [p.id for p in game.players if not p.is_bankrupt]
        game.active_auction = AuctionState(
            space_id=space_id,
            current_bid=100,
            highest_bidder_id=None,
            active_bidders=active_player_ids,
            expires_at=time.time() + 20.0
        )
        game.turn_phase = TurnPhase.AUCTION_IN_PROGRESS
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{cur.name} declined to buy {space.name}. Public auction started at ₹100!",
            hindi_message=f"{space.name} की सार्वजनिक नीलामी ₹100 से शुरू हुई!",
            log_type="property"
        ))
        return {"status": "auction_started", "auction": game.active_auction.model_dump()}

    @staticmethod
    def place_bid(game: GameState, player_id: str, bid_amount: int) -> Dict[str, Any]:
        if game.turn_phase != TurnPhase.AUCTION_IN_PROGRESS or not game.active_auction:
            return {"error": "No active auction"}

        player = next((p for p in game.players if p.id == player_id), None)
        if not player or player.is_bankrupt or player.cash < bid_amount:
            return {"error": "Invalid bidder or insufficient cash"}

        if bid_amount <= game.active_auction.current_bid:
            return {"error": "Bid must be higher than current bid"}

        game.active_auction.current_bid = bid_amount
        game.active_auction.highest_bidder_id = player_id
        game.active_auction.expires_at = time.time() + 10.0  # Reset 10s timer on new bid

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} bid ₹{bid_amount:,} in the auction!",
            player_id=player_id,
            log_type="property"
        ))
        return {"status": "bid_accepted", "auction": game.active_auction.model_dump()}

    @staticmethod
    def conclude_auction(game: GameState) -> Dict[str, Any]:
        if not game.active_auction:
            return {"error": "No auction"}

        space = get_space_by_id(game.active_auction.space_id)
        winner_id = game.active_auction.highest_bidder_id
        winning_bid = game.active_auction.current_bid

        if winner_id and space:
            winner = next((p for p in game.players if p.id == winner_id), None)
            if winner and winner.cash >= winning_bid:
                winner.cash -= winning_bid
                game.properties[space.id] = PropertyOwnership(
                    space_id=space.id,
                    owner_id=winner_id
                )
                game.logs.append(GameLog(
                    id=str(uuid.uuid4()),
                    message=f"{winner.name} won {space.name} in auction for ₹{winning_bid:,}!",
                    hindi_message=f"{winner.name} ने ₹{winning_bid:,} में नीलामी जीती!",
                    player_id=winner_id,
                    log_type="property"
                ))

        game.active_auction = None
        game.turn_phase = TurnPhase.POST_TURN
        return {"status": "auction_concluded"}

    @staticmethod
    def build_bhavan(game: GameState, player_id: str, space_id: int) -> Dict[str, Any]:
        player = next((p for p in game.players if p.id == player_id), None)
        if not player or player.is_bankrupt:
            return {"error": "Invalid player"}

        space = get_space_by_id(space_id)
        ownership = game.properties.get(space_id)
        if not space or not ownership or ownership.owner_id != player_id:
            return {"error": "You do not own this property"}

        if space.type != SpaceType.PROPERTY or ownership.has_mahal or ownership.bhavans >= 4:
            return {"error": "Cannot build more Bhavans here"}

        # Check Monopoly
        group = COLOR_GROUPS_MAP.get(space.color_group, [])
        for sid in group:
            own = game.properties.get(sid)
            if not own or own.owner_id != player_id or own.is_mortgaged:
                return {"error": "Must own entire un-mortgaged color group to build"}

        # Check Uniform Building Rule
        current_bhavans = ownership.bhavans
        for sid in group:
            own = game.properties.get(sid)
            if own.bhavans < current_bhavans:
                return {"error": "Must build evenly across all properties in color group"}

        if game.bank_bhavans <= 0:
            return {"error": "Building shortage! No Bhavans left in the Bank."}

        if player.cash < space.house_cost:
            return {"error": "Insufficient funds to construct Bhavan"}

        player.cash -= space.house_cost
        ownership.bhavans += 1
        game.bank_bhavans -= 1

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} built a Bhavan on {space.name} (Now {ownership.bhavans} Bhavans) for ₹{space.house_cost:,}.",
            player_id=player_id,
            log_type="property"
        ))
        return {"status": "built_bhavan", "bhavans": ownership.bhavans}

    @staticmethod
    def build_mahal(game: GameState, player_id: str, space_id: int) -> Dict[str, Any]:
        player = next((p for p in game.players if p.id == player_id), None)
        if not player or player.is_bankrupt:
            return {"error": "Invalid player"}

        space = get_space_by_id(space_id)
        ownership = game.properties.get(space_id)
        if not space or not ownership or ownership.owner_id != player_id:
            return {"error": "You do not own this property"}

        if ownership.bhavans != 4 or ownership.has_mahal:
            return {"error": "Must have exactly 4 Bhavans before building a Mahal"}

        if game.bank_mahals <= 0:
            return {"error": "No Mahals left in Bank supply!"}

        if player.cash < space.hotel_cost:
            return {"error": "Insufficient funds to erect Mahal"}

        player.cash -= space.hotel_cost
        ownership.bhavans = 0
        ownership.has_mahal = True
        game.bank_bhavans += 4  # Return 4 Bhavans to Bank
        game.bank_mahals -= 1

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} upgraded {space.name} to a luxury MAHAL for ₹{space.hotel_cost:,}!",
            hindi_message=f"{player.name} ने {space.name} पर भव्य महल स्थापित किया!",
            player_id=player_id,
            log_type="property"
        ))
        return {"status": "built_mahal"}

    @staticmethod
    def mortgage_property(game: GameState, player_id: str, space_id: int) -> Dict[str, Any]:
        space = get_space_by_id(space_id)
        ownership = game.properties.get(space_id)
        player = next((p for p in game.players if p.id == player_id), None)

        if not space or not ownership or not player or ownership.owner_id != player_id:
            return {"error": "Cannot mortgage property"}

        if ownership.is_mortgaged:
            return {"error": "Property is already mortgaged"}

        # Check if buildings exist in color group
        if space.type == SpaceType.PROPERTY:
            group = COLOR_GROUPS_MAP.get(space.color_group, [])
            for sid in group:
                own = game.properties.get(sid)
                if own and (own.bhavans > 0 or own.has_mahal):
                    return {"error": "Must sell all Bhavans/Mahals in color group before mortgaging"}

        ownership.is_mortgaged = True
        player.cash += space.mortgage_value

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} mortgaged {space.name} to the Bank for ₹{space.mortgage_value:,}.",
            player_id=player_id,
            log_type="cash"
        ))
        return {"status": "mortgaged", "cash_received": space.mortgage_value}

    @staticmethod
    def unmortgage_property(game: GameState, player_id: str, space_id: int) -> Dict[str, Any]:
        space = get_space_by_id(space_id)
        ownership = game.properties.get(space_id)
        player = next((p for p in game.players if p.id == player_id), None)

        if not space or not ownership or not player or ownership.owner_id != player_id:
            return {"error": "Cannot un-mortgage property"}

        if not ownership.is_mortgaged:
            return {"error": "Property is not mortgaged"}

        # 10% statutory interest
        unmortgage_cost = int(space.mortgage_value * 1.1)
        if player.cash < unmortgage_cost:
            return {"error": "Insufficient funds to un-mortgage (Need ₹{:,})".format(unmortgage_cost)}

        player.cash -= unmortgage_cost
        ownership.is_mortgaged = False

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} redeemed {space.name} from mortgage for ₹{unmortgage_cost:,}.",
            player_id=player_id,
            log_type="cash"
        ))
        return {"status": "unmortgaged", "cost": unmortgage_cost}

    @staticmethod
    def pay_jail_bail(game: GameState, player_id: str) -> Dict[str, Any]:
        player = next((p for p in game.players if p.id == player_id), None)
        if not player or not player.in_jail or game.current_player.id != player_id:
            return {"error": "Cannot pay bail"}

        if player.cash < 500:
            return {"error": "Insufficient cash for bail fine (₹500)"}

        player.cash -= 500
        player.in_jail = False
        player.jail_turns = 0
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} paid ₹500 legal bail fee and was released from Police Chowki.",
            player_id=player_id,
            log_type="jail"
        ))
        return {"status": "released_from_jail"}

    @staticmethod
    def use_jail_card(game: GameState, player_id: str) -> Dict[str, Any]:
        player = next((p for p in game.players if p.id == player_id), None)
        if not player or not player.in_jail or player.get_out_of_jail_cards <= 0:
            return {"error": "No Zamanat Patra card available"}

        player.get_out_of_jail_cards -= 1
        player.in_jail = False
        player.jail_turns = 0
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"{player.name} presented a Zamanat Patra (Bail Bond) and walked out of Police Chowki free!",
            hindi_message=f"{player.name} ने ज़मानत पत्र प्रस्तुत कर निःशुल्क रिहाई पाई!",
            player_id=player_id,
            log_type="jail"
        ))
        return {"status": "released_from_jail"}

    @staticmethod
    def _draw_card(game: GameState, player: Player, deck_type: str) -> Dict[str, Any]:
        deck_ids = game.kismat_deck if deck_type == SpaceType.KISMAT else game.panchayat_deck
        all_cards = KISMAT_CARDS if deck_type == SpaceType.KISMAT else PANCHAYAT_CARDS

        if not deck_ids:
            deck_ids = [c.id for c in all_cards]
            random.shuffle(deck_ids)
            if deck_type == SpaceType.KISMAT:
                game.kismat_deck = deck_ids
            else:
                game.panchayat_deck = deck_ids

        card_id = deck_ids.pop(0)
        deck_ids.append(card_id)  # Place at bottom
        card = next((c for c in all_cards if c.id == card_id), None)

        if not card:
            game.turn_phase = TurnPhase.POST_TURN
            return {"action": "card_error"}

        game.last_drawn_card = card.model_dump()
        deck_label = "Kismat (Luck)" if deck_type == SpaceType.KISMAT else "Panchayat Kalyan"
        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"[{deck_label}] {player.name} drew '{card.title}': {card.description}",
            hindi_message=f"[{deck_label}] '{card.hindi_title}': {card.description}",
            player_id=player.id,
            log_type="card"
        ))

        # Execute Card Effect
        if card.action_type == CardActionType.COLLECT_MONEY:
            player.cash += card.value
        elif card.action_type == CardActionType.PAY_MONEY:
            player.cash -= card.value
            KuberGameEngine._check_bankruptcy(game, player)
        elif card.action_type == CardActionType.COLLECT_FROM_PLAYERS:
            for p in game.players:
                if p.id != player.id and not p.is_bankrupt:
                    transfer = min(p.cash, card.value)
                    p.cash -= transfer
                    player.cash += transfer
        elif card.action_type == CardActionType.PAY_TO_PLAYERS:
            for p in game.players:
                if p.id != player.id and not p.is_bankrupt:
                    player.cash -= card.value
                    p.cash += card.value
            KuberGameEngine._check_bankruptcy(game, player)
        elif card.action_type == CardActionType.GET_OUT_OF_JAIL_FREE:
            player.get_out_of_jail_cards += 1
        elif card.action_type == CardActionType.GO_TO_JAIL:
            player.in_jail = True
            player.position = 10
            player.jail_turns = 0
            game.doubles_count = 0
        elif card.action_type == CardActionType.MOVE_TO_POSITION:
            old_pos = player.position
            target_pos = card.value
            if card.collect_salary_on_pass and target_pos < old_pos and target_pos != 0:
                player.cash += 2000
            player.position = target_pos
            target_space = get_space_by_id(target_pos)
            if target_space:
                return KuberGameEngine._resolve_landed_space(game, player, target_space)
        elif card.action_type == CardActionType.MOVE_STEPS:
            new_pos = (player.position + card.value) % 40
            player.position = new_pos
            target_space = get_space_by_id(new_pos)
            if target_space:
                return KuberGameEngine._resolve_landed_space(game, player, target_space)
        elif card.action_type == CardActionType.MOVE_TO_NEAREST_TRANSPORT:
            # Transports at 5, 15, 25, 35
            cur_p = player.position
            nearest = 5
            for t in [5, 15, 25, 35]:
                if t > cur_p:
                    nearest = t
                    break
            if nearest < cur_p:
                player.cash += 2000  # Passed GO
            player.position = nearest
            target_space = get_space_by_id(nearest)
            if target_space:
                return KuberGameEngine._resolve_landed_space(game, player, target_space)
        elif card.action_type == CardActionType.MOVE_TO_NEAREST_UTILITY:
            # Utilities at 12, 28
            cur_p = player.position
            nearest = 12 if cur_p < 12 or cur_p >= 28 else 28
            if nearest < cur_p:
                player.cash += 2000
            player.position = nearest
            target_space = get_space_by_id(nearest)
            if target_space:
                return KuberGameEngine._resolve_landed_space(game, player, target_space)
        elif card.action_type == CardActionType.PROPERTY_REPAIRS:
            total_bhavans = sum(
                own.bhavans for own in game.properties.values()
                if own.owner_id == player.id
            )
            total_mahals = sum(
                1 for own in game.properties.values()
                if own.owner_id == player.id and own.has_mahal
            )
            total_repair_cost = (total_bhavans * card.house_fee) + (total_mahals * card.hotel_fee)
            player.cash -= total_repair_cost
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"{player.name} assessed repair bill of ₹{total_repair_cost:,} ({total_bhavans} Bhavans, {total_mahals} Mahals).",
                player_id=player.id,
                log_type="cash"
            ))
            KuberGameEngine._check_bankruptcy(game, player)

        game.turn_phase = TurnPhase.POST_TURN
        return {"action": "card_resolved", "card": card.model_dump()}

    @staticmethod
    def end_turn(game: GameState, player_id: str) -> Dict[str, Any]:
        cur = game.current_player
        if not cur or cur.id != player_id:
            return {"error": "Not your turn"}

        # If rolled doubles and not in jail, player gets another turn!
        if game.doubles_count > 0 and not cur.in_jail and not cur.is_bankrupt:
            game.turn_phase = TurnPhase.PRE_ROLL
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"{cur.name} rolled doubles and takes another roll!",
                player_id=cur.id
            ))
            return {"status": "extra_turn"}

        game.doubles_count = 0
        active_players = [p for p in game.players if not p.is_bankrupt]

        # Victory Check
        if len(active_players) <= 1:
            winner = active_players[0] if active_players else game.players[0]
            game.status = "completed"
            game.winner_id = winner.id
            game.turn_phase = TurnPhase.GAME_OVER
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"VICTORY! {winner.name} has conquered all rivals to become the supreme KUBER OF INDIA!",
                hindi_message=f"विजय! {winner.name} ने सभी प्रतिद्वंद्वियों को पछाड़कर भारत के कुबेर का ताज पहना!",
                player_id=winner.id,
                log_type="alert"
            ))
            return {"status": "game_won", "winner_id": winner.id}

        # Rotate to next active player
        num_players = len(game.players)
        next_idx = (game.current_player_index + 1) % num_players
        while game.players[next_idx].is_bankrupt:
            next_idx = (next_idx + 1) % num_players

        game.current_player_index = next_idx
        game.turn_number += 1
        game.turn_phase = TurnPhase.PRE_ROLL
        next_player = game.players[next_idx]

        game.logs.append(GameLog(
            id=str(uuid.uuid4()),
            message=f"Turn passed to {next_player.name}.",
            player_id=next_player.id
        ))
        return {"status": "next_turn", "current_player_id": next_player.id}

    @staticmethod
    def _check_bankruptcy(game: GameState, player: Player, creditor: Optional[Player] = None):
        if player.cash >= 0:
            return

        # Calculate total liquidation value
        total_assets = player.cash
        for sid, own in list(game.properties.items()):
            if own.owner_id == player.id:
                space = get_space_by_id(sid)
                if space:
                    if not own.is_mortgaged:
                        total_assets += space.mortgage_value
                    total_assets += (own.bhavans * (space.house_cost // 2))
                    if own.has_mahal:
                        total_assets += (space.hotel_cost // 2)

        if total_assets < 0:
            # Bankruptcy Declared!
            player.is_bankrupt = True
            game.logs.append(GameLog(
                id=str(uuid.uuid4()),
                message=f"BANKRUPTCY! {player.name} has run out of funds and surrendered!",
                hindi_message=f"दिवालिया! {player.name} की सारी संपत्ति समाप्त हो गई!",
                player_id=player.id,
                log_type="alert"
            ))

            if creditor:
                # Transfer all properties to creditor
                for sid, own in list(game.properties.items()):
                    if own.owner_id == player.id:
                        own.owner_id = creditor.id
                        own.is_mortgaged = True
                if player.cash > 0:
                    creditor.cash += player.cash
                creditor.get_out_of_jail_cards += player.get_out_of_jail_cards
            else:
                # Bank foreclosure: clear properties for open auction
                for sid, own in list(game.properties.items()):
                    if own.owner_id == player.id:
                        del game.properties[sid]
