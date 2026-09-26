"""
Indian Monopoly (KUBER) - Board Data Model and Layout Specifications
"""
from typing import List, Dict, Optional
from pydantic import BaseModel

class SpaceType:
    PROPERTY = "property"
    TRANSPORT = "transport"
    UTILITY = "utility"
    KISMAT = "kismat"
    PANCHAYAT = "panchayat"
    TAX = "tax"
    GO = "go"
    JAIL = "jail"
    FREE_PARKING = "free_parking"
    GO_TO_JAIL = "go_to_jail"

class ColorGroup:
    BROWN = "Brown"          # Heritage Terracotta
    LIGHT_BLUE = "LightBlue"  # Coastal Cyan
    PINK = "Pink"            # Royal Magenta
    ORANGE = "Orange"        # Saffron Sunset
    RED = "Red"              # Crimson Festive
    YELLOW = "Yellow"        # Golden Ochre
    GREEN = "Green"          # Emerald Capital
    DARK_BLUE = "DarkBlue"   # Royal Indigo

class BoardSpace(BaseModel):
    id: int
    name: str
    hindi_name: str
    type: str
    color_group: Optional[str] = None
    price: int = 0
    base_rent: int = 0
    rent_1_house: int = 0
    rent_2_house: int = 0
    rent_3_house: int = 0
    rent_4_house: int = 0
    rent_hotel: int = 0
    house_cost: int = 0
    hotel_cost: int = 0
    mortgage_value: int = 0
    city: Optional[str] = None
    state: Optional[str] = None
    description: str = ""
    icon: str = ""

# Complete 40 Board Spaces
BOARD_SPACES: List[BoardSpace] = [
    # Bottom Row: 0 (Corner) to 10 (Corner) - Moving Left to Right
    BoardSpace(
        id=0,
        name="Aarambh (Start)",
        hindi_name="शुभ आरम्भ",
        type=SpaceType.GO,
        description="Auspicious Beginning. Collect ₹2,000 as salary upon passing or landing.",
        icon="sparkles"
    ),
    BoardSpace(
        id=1,
        name="Chandni Chowk",
        hindi_name="चाँदनी चौक",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.BROWN,
        price=600,
        base_rent=20,
        rent_1_house=100,
        rent_2_house=300,
        rent_3_house=900,
        rent_4_house=1600,
        rent_hotel=2500,
        house_cost=500,
        hotel_cost=500,
        mortgage_value=300,
        city="Old Delhi",
        state="Delhi",
        description="Mughal-era historic bazaar famous for spice markets and heritage trade.",
        icon="store"
    ),
    BoardSpace(
        id=2,
        name="Panchayat Kalyan",
        hindi_name="पंचायत कल्याण",
        type=SpaceType.PANCHAYAT,
        description="Draw a Panchayat & Community Welfare card.",
        icon="users"
    ),
    BoardSpace(
        id=3,
        name="Charminar Bazaar",
        hindi_name="चारमीनार बाज़ार",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.BROWN,
        price=600,
        base_rent=40,
        rent_1_house=200,
        rent_2_house=600,
        rent_3_house=1800,
        rent_4_house=3200,
        rent_hotel=4500,
        house_cost=500,
        hotel_cost=500,
        mortgage_value=300,
        city="Hyderabad",
        state="Telangana",
        description="Laad Bazaar pearl traders and historic monument surroundings.",
        icon="landmark"
    ),
    BoardSpace(
        id=4,
        name="Aaykar (Income Tax)",
        hindi_name="आयकर",
        type=SpaceType.TAX,
        price=2000,
        description="Pay statutory Income Tax of ₹2,000 to the Bank.",
        icon="receipt"
    ),
    BoardSpace(
        id=5,
        name="Howrah Junction",
        hindi_name="हावड़ा जंक्शन",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        city="Kolkata",
        state="West Bengal",
        description="Eastern Railway gateway connecting millions daily over the Hooghly.",
        icon="train"
    ),
    BoardSpace(
        id=6,
        name="Promenade Beach Rd",
        hindi_name="प्रोमेनेड बीच रोड",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.LIGHT_BLUE,
        price=1000,
        base_rent=60,
        rent_1_house=300,
        rent_2_house=900,
        rent_3_house=2700,
        rent_4_house=4000,
        rent_hotel=5500,
        house_cost=500,
        hotel_cost=500,
        mortgage_value=500,
        city="Puducherry",
        state="Puducherry",
        description="Scenic French-colonial seafront promenade and boutique heritage villas.",
        icon="palmtree"
    ),
    BoardSpace(
        id=7,
        name="Kismat (Luck)",
        hindi_name="किस्मत",
        type=SpaceType.KISMAT,
        description="Draw a Kismat (Luck & Destiny) card.",
        icon="clover"
    ),
    BoardSpace(
        id=8,
        name="Calangute Strip",
        hindi_name="कलंगूट स्ट्रिप",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.LIGHT_BLUE,
        price=1000,
        base_rent=60,
        rent_1_house=300,
        rent_2_house=900,
        rent_3_house=2700,
        rent_4_house=4000,
        rent_hotel=5500,
        house_cost=500,
        hotel_cost=500,
        mortgage_value=500,
        city="North Goa",
        state="Goa",
        description="High-energy beach tourist boulevard and resort strip.",
        icon="sun"
    ),
    BoardSpace(
        id=9,
        name="Marine Drive Kochi",
        hindi_name="मरीन ड्राइव कोच्चि",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.LIGHT_BLUE,
        price=1200,
        base_rent=80,
        rent_1_house=400,
        rent_2_house=1000,
        rent_3_house=3000,
        rent_4_house=4500,
        rent_hotel=6000,
        house_cost=500,
        hotel_cost=500,
        mortgage_value=600,
        city="Kochi",
        state="Kerala",
        description="Picturesque backwaters waterfront promenade and trade corridor.",
        icon="anchor"
    ),
    # Left Column: 10 (Corner) to 20 (Corner) - Moving Bottom to Top
    BoardSpace(
        id=10,
        name="Police Chowki",
        hindi_name="पुलिस चौकी / हवालात",
        type=SpaceType.JAIL,
        description="Detention Center. Just Visiting or Serving Bail Period.",
        icon="shield-alert"
    ),
    BoardSpace(
        id=11,
        name="MI Road (Pink City)",
        hindi_name="एमआई रोड",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.PINK,
        price=1400,
        base_rent=100,
        rent_1_house=500,
        rent_2_house=1500,
        rent_3_house=4500,
        rent_4_house=6250,
        rent_hotel=7500,
        house_cost=1000,
        hotel_cost=1000,
        mortgage_value=700,
        city="Jaipur",
        state="Rajasthan",
        description="Mirza Ismail Road, Jaipur's regal handicraft, gems and emporium boulevard.",
        icon="gem"
    ),
    BoardSpace(
        id=12,
        name="National Power Grid",
        hindi_name="राष्ट्रीय ऊर्जा ग्रिड",
        type=SpaceType.UTILITY,
        price=1500,
        mortgage_value=750,
        description="National Electricity Grid. Rent = 40x dice roll (1 owned) or 100x dice roll (both owned).",
        icon="zap"
    ),
    BoardSpace(
        id=13,
        name="Dashashwamedh Ghat",
        hindi_name="दशाश्वमेध घाट",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.PINK,
        price=1400,
        base_rent=100,
        rent_1_house=500,
        rent_2_house=1500,
        rent_3_house=4500,
        rent_4_house=6250,
        rent_hotel=7500,
        house_cost=1000,
        hotel_cost=1000,
        mortgage_value=700,
        city="Varanasi",
        state="Uttar Pradesh",
        description="World's most iconic spiritual riverfront and heritage pilgrimage center.",
        icon="flame"
    ),
    BoardSpace(
        id=14,
        name="Mall Road Shimla",
        hindi_name="माल रोड शिमला",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.PINK,
        price=1600,
        base_rent=120,
        rent_1_house=600,
        rent_2_house=1800,
        rent_3_house=5000,
        rent_4_house=7000,
        rent_hotel=9000,
        house_cost=1000,
        hotel_cost=1000,
        mortgage_value=800,
        city="Shimla",
        state="Himachal Pradesh",
        description="Himalayan ridge pedestrian shopping promenade and colonial retreat.",
        icon="mountain"
    ),
    BoardSpace(
        id=15,
        name="CSMT Terminus",
        hindi_name="सीएसएमटी मुंबई",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        city="Mumbai",
        state="Maharashtra",
        description="UNESCO World Heritage Victorian Gothic landmark and Central Railway HQ.",
        icon="train"
    ),
    BoardSpace(
        id=16,
        name="FC Road (Deccan)",
        hindi_name="एफसी रोड पुणे",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.ORANGE,
        price=1800,
        base_rent=140,
        rent_1_house=700,
        rent_2_house=2000,
        rent_3_house=5500,
        rent_4_house=7500,
        rent_hotel=9500,
        house_cost=1000,
        hotel_cost=1000,
        mortgage_value=900,
        city="Pune",
        state="Maharashtra",
        description="Fergusson College Road, vibrant youth cafe and educational-commercial strip.",
        icon="coffee"
    ),
    BoardSpace(
        id=17,
        name="Panchayat Kalyan",
        hindi_name="पंचायत कल्याण",
        type=SpaceType.PANCHAYAT,
        description="Draw a Panchayat & Community Welfare card.",
        icon="users"
    ),
    BoardSpace(
        id=18,
        name="CG Road",
        hindi_name="सीजी रोड अहमदाबाद",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.ORANGE,
        price=1800,
        base_rent=140,
        rent_1_house=700,
        rent_2_house=2000,
        rent_3_house=5500,
        rent_4_house=7500,
        rent_hotel=9500,
        house_cost=1000,
        hotel_cost=1000,
        mortgage_value=900,
        city="Ahmedabad",
        state="Gujarat",
        description="Chimanlal Girdharlal Road, prime retail and enterprise avenue.",
        icon="briefcase"
    ),
    BoardSpace(
        id=19,
        name="Sector 17 Plaza",
        hindi_name="सेक्टर 17 प्लाज़ा",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.ORANGE,
        price=2000,
        base_rent=160,
        rent_1_house=800,
        rent_2_house=2200,
        rent_3_house=6000,
        rent_4_house=8000,
        rent_hotel=10000,
        house_cost=1000,
        hotel_cost=1000,
        mortgage_value=1000,
        city="Chandigarh",
        state="Chandigarh",
        description="Le Corbusier planned pedestrian shopping hub with open courtyards.",
        icon="building"
    ),
    # Top Row: 20 (Corner) to 30 (Corner) - Moving Left to Right
    BoardSpace(
        id=20,
        name="Vishram Sthal",
        hindi_name="विश्राम स्थल (यात्री निवास)",
        type=SpaceType.FREE_PARKING,
        description="Free Resting Zone. Relax and plan your next tycoon investment.",
        icon="tent"
    ),
    BoardSpace(
        id=21,
        name="Park Street",
        hindi_name="पार्क स्ट्रीट",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.RED,
        price=2200,
        base_rent=180,
        rent_1_house=900,
        rent_2_house=2500,
        rent_3_house=7000,
        rent_4_house=8750,
        rent_hotel=10500,
        house_cost=1500,
        hotel_cost=1500,
        mortgage_value=1100,
        city="Kolkata",
        state="West Bengal",
        description="The cultural, culinary, and nightlife high-street of the City of Joy.",
        icon="music"
    ),
    BoardSpace(
        id=22,
        name="Kismat (Luck)",
        hindi_name="किस्मत",
        type=SpaceType.KISMAT,
        description="Draw a Kismat (Luck & Destiny) card.",
        icon="clover"
    ),
    BoardSpace(
        id=23,
        name="HITEC City Cyber Towers",
        hindi_name="हाईटेक सिटी",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.RED,
        price=2200,
        base_rent=180,
        rent_1_house=900,
        rent_2_house=2500,
        rent_3_house=7000,
        rent_4_house=8750,
        rent_hotel=10500,
        house_cost=1500,
        hotel_cost=1500,
        mortgage_value=1100,
        city="Hyderabad",
        state="Telangana",
        description="Cyberabad flagship technology park housing global software giants.",
        icon="cpu"
    ),
    BoardSpace(
        id=24,
        name="Brigade & MG Road",
        hindi_name="ब्रिगेड और एमजी रोड",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.RED,
        price=2400,
        base_rent=200,
        rent_1_house=1000,
        rent_2_house=3000,
        rent_3_house=7500,
        rent_4_house=9250,
        rent_hotel=11000,
        house_cost=1500,
        hotel_cost=1500,
        mortgage_value=1200,
        city="Bengaluru",
        state="Karnataka",
        description="Silicon Plateau's bustling commercial core, pubs, and tech headquarters.",
        icon="laptop"
    ),
    BoardSpace(
        id=25,
        name="New Delhi Junction",
        hindi_name="नई दिल्ली रेलवे स्टेशन",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        city="New Delhi",
        state="Delhi",
        description="Northern Railway mega-terminus handling over 500,000 travelers daily.",
        icon="train"
    ),
    BoardSpace(
        id=26,
        name="T. Nagar & Anna Salai",
        hindi_name="टी. नगर और अन्ना सलाई",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.YELLOW,
        price=2600,
        base_rent=220,
        rent_1_house=1100,
        rent_2_house=3300,
        rent_3_house=8000,
        rent_4_house=9750,
        rent_hotel=11500,
        house_cost=1500,
        hotel_cost=1500,
        mortgage_value=1300,
        city="Chennai",
        state="Tamil Nadu",
        description="India's largest retail silk and gold jewelry shopping district.",
        icon="shopping-bag"
    ),
    BoardSpace(
        id=27,
        name="Golf Course Road",
        hindi_name="गोल्फ कोर्स रोड",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.YELLOW,
        price=2600,
        base_rent=220,
        rent_1_house=1100,
        rent_2_house=3300,
        rent_3_house=8000,
        rent_4_house=9750,
        rent_hotel=11500,
        house_cost=1500,
        hotel_cost=1500,
        mortgage_value=1300,
        city="Gurugram",
        state="Haryana",
        description="Millennium City's ultra-luxury condominium and corporate glass tower corridor.",
        icon="building-2"
    ),
    BoardSpace(
        id=28,
        name="Jal Jeevan Board",
        hindi_name="जल जीवन जल बोर्ड",
        type=SpaceType.UTILITY,
        price=1500,
        mortgage_value=750,
        description="National Water Infrastructure. Rent = 40x dice roll (1 owned) or 100x dice roll (both owned).",
        icon="droplets"
    ),
    BoardSpace(
        id=29,
        name="GS Road (Dispur Hub)",
        hindi_name="जीएस रोड गुवाहाटी",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.YELLOW,
        price=2800,
        base_rent=240,
        rent_1_house=1200,
        rent_2_house=3600,
        rent_3_house=8500,
        rent_4_house=10250,
        rent_hotel=12000,
        house_cost=1500,
        hotel_cost=1500,
        mortgage_value=1400,
        city="Guwahati",
        state="Assam",
        description="Northeast India's premier commercial and hospitality expressway.",
        icon="map-pin"
    ),
    # Right Column: 30 (Corner) to 39 - Moving Top to Bottom
    BoardSpace(
        id=30,
        name="Nyayalay Saman",
        hindi_name="न्यायालय समन (हवालात जाएं)",
        type=SpaceType.GO_TO_JAIL,
        description="Court summons issued! Advance directly to Police Chowki without collecting ₹2,000 salary.",
        icon="gavel"
    ),
    BoardSpace(
        id=31,
        name="Connaught Place",
        hindi_name="कनॉट प्लेस",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.GREEN,
        price=3000,
        base_rent=260,
        rent_1_house=1300,
        rent_2_house=3900,
        rent_3_house=9000,
        rent_4_house=11000,
        rent_hotel=12750,
        house_cost=2000,
        hotel_cost=2000,
        mortgage_value=1500,
        city="New Delhi",
        state="Delhi",
        description="Iconic circular Georgian colonial colonnade and corporate nerve center.",
        icon="compass"
    ),
    BoardSpace(
        id=32,
        name="Bandra-Kurla Complex",
        hindi_name="बांद्रा-कुर्ला कॉम्प्लेक्स (BKC)",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.GREEN,
        price=3000,
        base_rent=260,
        rent_1_house=1300,
        rent_2_house=3900,
        rent_3_house=9000,
        rent_4_house=11000,
        rent_hotel=12750,
        house_cost=2000,
        hotel_cost=2000,
        mortgage_value=1500,
        city="Mumbai",
        state="Maharashtra",
        description="India's highest valued central financial district and corporate headquarters.",
        icon="landmark"
    ),
    BoardSpace(
        id=33,
        name="Panchayat Kalyan",
        hindi_name="पंचायत कल्याण",
        type=SpaceType.PANCHAYAT,
        description="Draw a Panchayat & Community Welfare card.",
        icon="users"
    ),
    BoardSpace(
        id=34,
        name="Lutyens' Bungalow Zone",
        hindi_name="लुटियंस बंगला ज़ोन",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.GREEN,
        price=3200,
        base_rent=280,
        rent_1_house=1500,
        rent_2_house=4500,
        rent_3_house=10000,
        rent_4_house=12000,
        rent_hotel=14000,
        house_cost=2000,
        hotel_cost=2000,
        mortgage_value=1600,
        city="New Delhi",
        state="Delhi",
        description="The nation's most elite diplomatic power corridors and sprawling estate grounds.",
        icon="crown"
    ),
    BoardSpace(
        id=35,
        name="Chennai Central MGR",
        hindi_name="चेन्नई सेंट्रल",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        city="Chennai",
        state="Tamil Nadu",
        description="Southern Railway's majestic crimson Romanesque transit nexus.",
        icon="train"
    ),
    BoardSpace(
        id=36,
        name="Kismat (Luck)",
        hindi_name="किस्मत",
        type=SpaceType.KISMAT,
        description="Draw a Kismat (Luck & Destiny) card.",
        icon="clover"
    ),
    BoardSpace(
        id=37,
        name="Altamount Road",
        hindi_name="अल्टामाउंट रोड",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.DARK_BLUE,
        price=3500,
        base_rent=350,
        rent_1_house=1750,
        rent_2_house=5000,
        rent_3_house=11000,
        rent_4_house=13000,
        rent_hotel=15000,
        house_cost=2000,
        hotel_cost=2000,
        mortgage_value=1750,
        city="Mumbai",
        state="Maharashtra",
        description="Billionaires' Boulevard on Cumballa Hill, home to India's wealthiest magnates.",
        icon="diamond"
    ),
    BoardSpace(
        id=38,
        name="GST & Luxury Cess",
        hindi_name="जीएसटी व विलासिता उपकर",
        type=SpaceType.TAX,
        price=1000,
        description="Pay statutory Luxury Goods & High-Wealth Cess of ₹1,000 to the Bank.",
        icon="badge-dollar-sign"
    ),
    BoardSpace(
        id=39,
        name="Marine Drive Promenade",
        hindi_name="मरीन ड्राइव मुंबई",
        type=SpaceType.PROPERTY,
        color_group=ColorGroup.DARK_BLUE,
        price=4000,
        base_rent=500,
        rent_1_house=2000,
        rent_2_house=6000,
        rent_3_house=14000,
        rent_4_house=17000,
        rent_hotel=20000,
        house_cost=2000,
        hotel_cost=2000,
        mortgage_value=2000,
        city="Mumbai",
        state="Maharashtra",
        description="The iconic Queen's Necklace waterfront arc and crown jewel of Indian real estate.",
        icon="sparkle"
    )
]

# Color Group Mapping
COLOR_GROUPS_MAP = {
    ColorGroup.BROWN: [1, 3],
    ColorGroup.LIGHT_BLUE: [6, 8, 9],
    ColorGroup.PINK: [11, 13, 14],
    ColorGroup.ORANGE: [16, 18, 19],
    ColorGroup.RED: [21, 23, 24],
    ColorGroup.YELLOW: [26, 27, 29],
    ColorGroup.GREEN: [31, 32, 34],
    ColorGroup.DARK_BLUE: [37, 39],
}

TRANSPORT_SPACES = [5, 15, 25, 35]
UTILITY_SPACES = [12, 28]

def get_space_by_id(space_id: int) -> Optional[BoardSpace]:
    for space in BOARD_SPACES:
        if space.id == space_id:
            return space
    return None
