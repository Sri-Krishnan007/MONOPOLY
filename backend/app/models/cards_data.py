"""
Indian Monopoly (KUBER) - Kismat (Luck) and Panchayat (Community) Card Models and Decks
"""
from typing import List, Optional
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
    deck: str  # "kismat" or "panchayat"
    title: str
    hindi_title: str
    description: str
    action_type: str
    value: int = 0  # Money amount or position index or step count
    house_fee: int = 0
    hotel_fee: int = 0
    collect_salary_on_pass: bool = True

KISMAT_CARDS: List[GameCard] = [
    GameCard(
        id="K01",
        deck="kismat",
        title="Shubh Yatra",
        hindi_title="शुभ यात्रा",
        description="Advance directly to Aarambh (GO). Collect ₹2,000 seasonal salary!",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=0,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="K02",
        deck="kismat",
        title="Vande Bharat Express",
        hindi_title="वंदे भारत एक्सप्रेस",
        description="Board the express! Advance directly to CSMT Terminus Mumbai. If you pass Aarambh, collect ₹2,000.",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=15,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="K03",
        deck="kismat",
        title="Billionaire's Row",
        hindi_title="अरबपतियों की नगरी",
        description="Fly to Marine Drive Promenade Mumbai. Buy it if unowned, or pay the owner their rent!",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=39,
        collect_salary_on_pass=False
    ),
    GameCard(
        id="K04",
        deck="kismat",
        title="Cyber Tech Boom",
        hindi_title="साइबर टेक उछाल",
        description="Advance token to Golf Course Road Gurugram. If you pass Aarambh, collect ₹2,000.",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=27,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="K05",
        deck="kismat",
        title="Smart Grid Surge",
        hindi_title="ऊर्जा मांग में उछाल",
        description="Advance token to nearest Utility. If unowned, buy it. If owned, throw dice and pay 100x roll!",
        action_type=CardActionType.MOVE_TO_NEAREST_UTILITY
    ),
    GameCard(
        id="K06",
        deck="kismat",
        title="Express Festive Rush",
        hindi_title="त्योहार एक्सप्रेस रश",
        description="Advance token to the nearest Transportation Hub. If owned, pay owner twice normal rent!",
        action_type=CardActionType.MOVE_TO_NEAREST_TRANSPORT
    ),
    GameCard(
        id="K07",
        deck="kismat",
        title="Traffic E-Challan",
        hindi_title="ई-चालान",
        description="Caught overspeeding on the Expressway. Pay fine of ₹150 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=150
    ),
    GameCard(
        id="K08",
        deck="kismat",
        title="Startup IPO Dividend",
        hindi_title="स्टार्टअप लाभांश",
        description="Your tech venture went public! Bank pays you a special dividend of ₹500.",
        action_type=CardActionType.COLLECT_MONEY,
        value=500
    ),
    GameCard(
        id="K09",
        deck="kismat",
        title="Diwali Home Renovation",
        hindi_title="दिवाली गृह नवीनीकरण",
        description="Pre-Diwali home repairs: Pay ₹250 for each Bhavan (House) and ₹1,000 for each Mahal (Hotel) you own.",
        action_type=CardActionType.PROPERTY_REPAIRS,
        house_fee=250,
        hotel_fee=1000
    ),
    GameCard(
        id="K10",
        deck="kismat",
        title="Zamanat Patra (Bail Bond)",
        hindi_title="ज़मानत पत्र",
        description="Get Out of Police Chowki Free! This card may be kept until needed or traded to another player.",
        action_type=CardActionType.GET_OUT_OF_JAIL_FREE
    ),
    GameCard(
        id="K11",
        deck="kismat",
        title="Tax Non-Compliance Warrant",
        hindi_title="न्यायिक समन",
        description="Tax inquiry notice issued! Advance directly to Police Chowki. Do not pass Aarambh, do not collect ₹2,000.",
        action_type=CardActionType.GO_TO_JAIL
    ),
    GameCard(
        id="K12",
        deck="kismat",
        title="GST Input Credit Refund",
        hindi_title="जीएसटी रिफंड",
        description="Annual tax audit cleared with full compliance! Collect ₹1,500 tax refund from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1500
    ),
    GameCard(
        id="K13",
        deck="kismat",
        title="Monsoon Waterlogging",
        hindi_title="मानसून जलभराव",
        description="Roads flooded during heavy monsoon showers. Step back 3 spaces.",
        action_type=CardActionType.MOVE_STEPS,
        value=-3
    ),
    GameCard(
        id="K14",
        deck="kismat",
        title="Wedding Shagun (Sangeet)",
        hindi_title="शादी शगुन",
        description="Daughter's wedding celebration! Pay ₹500 to every player as celebratory sweets and shagun.",
        action_type=CardActionType.PAY_TO_PLAYERS,
        value=500
    ),
    GameCard(
        id="K15",
        deck="kismat",
        title="Festive Bonus (Diwali)",
        hindi_title="त्योहारी बोनस",
        description="Company declares annual festive bonus. Collect ₹1,000 from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="K16",
        deck="kismat",
        title="Heritage Conservation Cess",
        hindi_title="विरासत संरक्षण उपकर",
        description="Municipal heritage body levies building cess: Pay ₹400 per House and ₹1,150 per Hotel.",
        action_type=CardActionType.PROPERTY_REPAIRS,
        house_fee=400,
        hotel_fee=1150
    ),
]

PANCHAYAT_CARDS: List[GameCard] = [
    GameCard(
        id="P01",
        deck="panchayat",
        title="Gram Vikas Grant",
        hindi_title="ग्राम विकास अनुदान",
        description="Advance directly to Aarambh (GO). Collect ₹2,000 development salary.",
        action_type=CardActionType.MOVE_TO_POSITION,
        value=0,
        collect_salary_on_pass=True
    ),
    GameCard(
        id="P02",
        deck="panchayat",
        title="Kisan Agro Yield",
        hindi_title="कृषि उपज लाभ",
        description="Bountiful agricultural export harvest. Collect ₹1,000 from the Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="P03",
        deck="panchayat",
        title="Hospital Care Bill",
        hindi_title="चिकित्सा व्यय",
        description="Settle private specialty hospital bill. Pay ₹1,000 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=1000
    ),
    GameCard(
        id="P04",
        deck="panchayat",
        title="TDS Interest Refund",
        hindi_title="टीडीएस वापसी",
        description="Income Tax Department refunds excess tax deducted with interest. Collect ₹200.",
        action_type=CardActionType.COLLECT_MONEY,
        value=200
    ),
    GameCard(
        id="P05",
        deck="panchayat",
        title="Anticipatory Bail Bond",
        hindi_title="अग्रिम ज़मानत पत्र",
        description="Get Out of Police Chowki Free! This card may be kept or traded to other tycoons.",
        action_type=CardActionType.GET_OUT_OF_JAIL_FREE
    ),
    GameCard(
        id="P06",
        deck="panchayat",
        title="Lok Adalat Summons",
        hindi_title="लोक अदालत समन",
        description="Compliance inquiry notice. Move directly to Police Chowki (Detention). Do not pass Aarambh.",
        action_type=CardActionType.GO_TO_JAIL
    ),
    GameCard(
        id="P07",
        deck="panchayat",
        title="Grand Family Banquet",
        hindi_title="पारिवारिक दावत",
        description="Host celebratory anniversary banquet. Collect ₹100 from every player.",
        action_type=CardActionType.COLLECT_FROM_PLAYERS,
        value=100
    ),
    GameCard(
        id="P08",
        deck="panchayat",
        title="Maha-Utsav Sweets Seva",
        hindi_title="महा-उत्सव सेवा",
        description="Sponsor sweets and decorations for neighborhood festival. Pay ₹500 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=500
    ),
    GameCard(
        id="P09",
        deck="panchayat",
        title="Post Office NSC Deposit",
        hindi_title="राष्ट्रीय बचत पत्र",
        description="Your 5-Year National Savings Certificate matures with compound interest! Collect ₹1,000.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="P10",
        deck="panchayat",
        title="Solar Rooftop Subsidy",
        hindi_title="सौर ऊर्जा सब्सिडी",
        description="State Renewable Energy Agency approves green subsidy grant. Collect ₹1,000 from Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="P11",
        deck="panchayat",
        title="Colony Drain Repairs",
        hindi_title="नाली व सड़क मरम्मत",
        description="RWA infrastructure maintenance levy: Pay ₹400 for each Bhavan and ₹1,150 for each Mahal.",
        action_type=CardActionType.PROPERTY_REPAIRS,
        house_fee=400,
        hotel_fee=1150
    ),
    GameCard(
        id="P12",
        deck="panchayat",
        title="Civil Services Merit Award",
        hindi_title="सिविल सेवा सम्मान",
        description="Honored with State Administrative Fellowship. Collect ₹500 merit award from Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=500
    ),
    GameCard(
        id="P13",
        deck="panchayat",
        title="Education Tuition Fee",
        hindi_title="शिक्षा शुल्क",
        description="Pay university and school semester tuition fee. Pay ₹500 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=500
    ),
    GameCard(
        id="P14",
        deck="panchayat",
        title="Smart City Consultancy",
        hindi_title="परामर्श मानदेय",
        description="Acted as strategic advisor for Municipal Smart City project. Collect ₹250 honorarium.",
        action_type=CardActionType.COLLECT_MONEY,
        value=250
    ),
    GameCard(
        id="P15",
        deck="panchayat",
        title="Bazaar Stall Rental Yield",
        hindi_title="बाज़ार दुकान किराया",
        description="Collect commercial market shop quarterly rental dividend. Collect ₹1,000 from Bank.",
        action_type=CardActionType.COLLECT_MONEY,
        value=1000
    ),
    GameCard(
        id="P16",
        deck="panchayat",
        title="Langar & Annadanam Seva",
        hindi_title="लंगर व अन्नदानम् सेवा",
        description="Sponsor community kitchen meals. Sacred charitable donation: Pay ₹500 to the Bank.",
        action_type=CardActionType.PAY_MONEY,
        value=500
    ),
]
