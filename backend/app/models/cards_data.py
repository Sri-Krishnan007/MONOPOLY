"""
Indian Monopoly - Chance & Community Chest Card Decks (English Standard)
"""
from typing import List
from pydantic import BaseModel

class CardActionType:
    MOVE_TO_POSITION = "move_to_position"
    MOVE_TO_NEAREST_UTILITY = "move_to_nearest_utility"
    MOVE_TO_NEAREST_TRANSPORT = "move_to_nearest_transport"
    MOVE_STEPS = "move_steps"
    COLLECT_MONEY = "collect_money"
    PAY_MONEY = "pay_money"
    COLLECT_FROM_PLAYERS = "collect_from_players"
    PAY_TO_PLAYERS = "pay_to_players"
    PROPERTY_REPAIRS = "property_repairs"
    GO_TO_JAIL = "go_to_jail"
    GET_OUT_OF_JAIL_FREE = "get_out_of_jail_free"

class GameCard(BaseModel):
    id: str
    deck: str  # "chance" or "community"
    title: str
    description: str
    action_type: str
    value: int = 0
    house_fee: int = 0
    hotel_fee: int = 0
    collect_salary_on_pass: bool = True

CHANCE_CARDS: List[GameCard] = [
    GameCard(
        id="C01",
        deck="chance",
        title="Advance to GO",
        description="Advance directly to START / GO. Collect ₹2,000 salary!",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=0,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="C02",
        deck="chance",
        title="Vande Bharat Express",
        description="Board the express! Advance to CSMT Terminus Mumbai. If you pass GO, collect ₹2,000.",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=15,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="C03",
        deck="chance",
        title="Take a Walk on Marine Drive",
        description="Advance token to Marine Drive Promenade Mumbai.",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=39,
        collect_salary_on_pass=False
    ),
    GameCard(
        id="C04",
        deck="chance",
        title="Advance to Cyber City",
        description="Advance to Golf Course Road Gurugram. If you pass GO, collect ₹2,000.",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=27,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="C05",
        deck="chance",
        title="Infrastructure Demand Surge",
        description="Advance to the nearest Utility. If unowned, you may buy it. If owned, roll dice and pay 100x roll!",
        action_type=CardActionType.MOVE_TO_NEAREST_UTILITY
    ),
    GameCard(
        id="C06",
        deck="chance",
        title="Festival Travel Rush",
        description="Advance to the nearest Transportation Hub. If owned, pay owner twice normal rent!",
        action_type=CardActionType.MOVE_TO_NEAREST_TRANSPORT
    ),
    GameCard(
        id="C07",
        deck="chance",
        title="Expressway Speeding Fine",
        description="Automated speed camera violation. Pay ₹150 fine to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=150
    ),
    GameCard(
        id="C08",
        deck="chance",
        title="Tech Startup IPO Dividend",
        description="Your startup investment went public! Bank pays you ₹500 dividend.",
        action_type=CardActionType.COLLECT_MONEY,
        value=500
    ),
    GameCard(
        id="C09",
        deck="chance",
        title="General Property Renovation",
        description="Make general repairs on all your properties: Pay ₹250 for each House and ₹1,000 for each Hotel.",
        action_type=CardActionType.PROPERTY_REPAIRS,
        house_fee=250,
        hotel_fee=1000
    ),
    GameCard(
        id="C10",
        deck="chance",
        title="Get Out of Jail Free",
        description="This card may be kept until needed or traded to another player.",
        action_type=CardActionType.GET_OUT_OF_JAIL_FREE
    ),
    GameCard(
        id="C11",
        deck="chance",
        title="Go Directly to Jail",
        description="Court summons issued! Go directly to Jail. Do not pass GO, do not collect ₹2,000.",
        action_type=CardActionType.GO_TO_JAIL
    ),
    GameCard(
        id="C12",
        deck="chance",
        title="Tax Audit Refund",
        description="Annual tax audit completed successfully! Collect ₹1,500 refund from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1500
    ),
    GameCard(
        id="C13",
        deck="chance",
        title="Monsoon Waterlogging Delay",
        description="Flooded roads during heavy showers. Go back 3 spaces.",
        action_type=CardActionType.MOVE_STEPS,
        value=-3
    ),
    GameCard(
        id="C14",
        deck="chance",
        title="Elected Chairman of Board",
        description="Pay each player ₹500 as celebratory banquet gift.",
        action_type=CardActionType.PAY_TO_PLAYERS,
        value=500
    ),
    GameCard(
        id="C15",
        deck="chance",
        title="Festive Season Bonus",
        description="Corporate festive bonus distributed! Collect ₹1,000 from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="C16",
        deck="chance",
        title="Heritage Conservation Assessment",
        description="Municipal heritage body assessment: Pay ₹400 per House and ₹1,150 per Hotel.",
        action_type=CardActionType.PROPERTY_REPAIRS,
        house_fee=400,
        hotel_fee=1150
    ),
]

COMMUNITY_CARDS: List[GameCard] = [
    GameCard(
        id="CC01",
        deck="community",
        title="Advance to GO",
        description="Advance directly to START / GO. Collect ₹2,000 salary!",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=0,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="CC02",
        deck="community",
        title="Agricultural Venture Profit",
        description="Bountiful organic agricultural harvest. Collect ₹1,000 from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="CC03",
        deck="community",
        title="Doctor's Hospital Fee",
        description="Settle private specialty medical bill. Pay ₹1,000 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=1000
    ),
    GameCard(
        id="CC04",
        deck="community",
        title="Income Tax Error Refund",
        description="Income tax department refunds excess tax deduction with interest. Collect ₹200.",
        action_type=CardActionType.COLLECT_MONEY,
        value=200
    ),
    GameCard(
        id="CC05",
        deck="community",
        title="Get Out of Jail Free",
        description="This card may be kept until needed or traded to another tycoon.",
        action_type=CardActionType.GET_OUT_OF_JAIL_FREE
    ),
    GameCard(
        id="CC06",
        deck="community",
        title="Go to Jail",
        description="Go directly to Jail. Do not pass GO, do not collect ₹2,000.",
        action_type=CardActionType.GO_TO_JAIL
    ),
    GameCard(
        id="CC07",
        deck="community",
        title="Grand Anniversary Banquet",
        description="Host celebratory anniversary dinner. Collect ₹100 from every player.",
        action_type=CardActionType.COLLECT_FROM_PLAYERS,
        value=100
    ),
    GameCard(
        id="CC08",
        deck="community",
        title="Holiday Fund Matures",
        description="Receive ₹500 holiday festive payout from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=500
    ),
    GameCard(
        id="CC09",
        deck="community",
        title="Fixed Deposit Maturity",
        description="Your 5-year fixed deposit matures with compound interest! Collect ₹1,000.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="CC10",
        deck="community",
        title="Solar Energy Subsidy",
        description="Renewable energy rooftop subsidy granted. Collect ₹1,000 from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="CC11",
        deck="community",
        title="Colony Street Repairs",
        description="RWA maintenance fee: Pay ₹400 for each House and ₹1,150 for each Hotel.",
        action_type=CardActionType.PROPERTY_REPAIRS,
        house_fee=400,
        hotel_fee=1150
    ),
    GameCard(
        id="CC12",
        deck="community",
        title="Merit Scholarship Award",
        description="Won prestigious state academic merit fellowship. Collect ₹500 from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=500
    ),
    GameCard(
        id="CC13",
        deck="community",
        title="School & College Tuition",
        description="Pay semester tuition and academic fees. Pay ₹500 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=500
    ),
    GameCard(
        id="CC14",
        deck="community",
        title="Consultancy Honorarium",
        description="Acted as strategic advisor for Municipal Smart City initiative. Collect ₹250 fee.",
        action_type=CardActionType.COLLECT_MONEY,
        value=250
    ),
    GameCard(
        id="CC15",
        deck="community",
        title="Commercial Property Rent Yield",
        description="Collect quarterly rent yield from commercial arcade shops. Collect ₹1,000.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="CC16",
        deck="community",
        title="Charitable Hospital Donation",
        description="Community kitchen and medical donation. Pay ₹500 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=500
    ),
]
