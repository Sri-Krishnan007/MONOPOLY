"""
Indian Monopoly - Board Data Model with Iconic Indian Cities and Monuments (English Standard)
"""
from typing import List, Dict, Optional
from pydantic import BaseModel

class SpaceType:
    PROPERTY = "property"
    TRANSPORT = "transport"
    UTILITY = "utility"
    CHANCE = "chance"
    COMMUNITY = "community"
    TAX = "tax"
    GO = "go"
    JAIL = "jail"
    FREE_PARKING = "free_parking"
    GO_TO_JAIL = "go_to_jail"

class ColorGroup:
    BROWN = "Brown"
    LIGHT_BLUE = "LightBlue"
    PINK = "Pink"
    ORANGE = "Orange"
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    DARK_BLUE = "DarkBlue"

class BoardSpace(BaseModel):
    id: int
    name: str
    monument: str
    city: str
    state: str
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
    description: str = ""
    icon: str = ""

# Complete 40 Board Spaces - Hasbro Monopoly Mathematical Standard
BOARD_SPACES: List[BoardSpace] = [
    # Bottom Row: 0 (GO) to 10 (Jail)
    BoardSpace(
        id=0,
        name="START / GO",
        monument="National Gateway",
        city="National",
        state="India",
        type=SpaceType.GO,
        description="Collect ₹2,000 salary upon passing or landing.",
        icon="sparkles"
    ),
    BoardSpace(
        id=1,
        name="Chandni Chowk",
        monument="Red Fort & Old Bazaar",
        city="Old Delhi",
        state="Delhi",
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
        description="Historic Mughal bazaar famous for commerce, spice markets, and heritage.",
        icon="landmark"
    ),
    BoardSpace(
        id=2,
        name="Community Chest",
        monument="Community Welfare",
        city="National",
        state="India",
        type=SpaceType.COMMUNITY,
        description="Draw a Community Chest Card.",
        icon="users"
    ),
    BoardSpace(
        id=3,
        name="Charminar Bazaar",
        monument="Charminar & Laad Bazaar",
        city="Hyderabad",
        state="Telangana",
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
        description="Iconic 16th-century four-minaret monument and famous pearl markets.",
        icon="monument"
    ),
    BoardSpace(
        id=4,
        name="Income Tax",
        monument="Direct Tax Office",
        city="Central",
        state="Revenue",
        type=SpaceType.TAX,
        price=2000,
        description="Pay statutory Income Tax of ₹2,000 to the Bank.",
        icon="receipt"
    ),
    BoardSpace(
        id=5,
        name="Howrah Junction",
        monument="Howrah Bridge & Station",
        city="Kolkata",
        state="West Bengal",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        description="Eastern Railway landmark and one of the world's busiest historic stations.",
        icon="train"
    ),
    BoardSpace(
        id=6,
        name="Promenade Beach",
        monument="French War Memorial",
        city="Puducherry",
        state="Puducherry",
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
        description="Scenic French-colonial coastal boulevard and heritage quarter.",
        icon="palmtree"
    ),
    BoardSpace(
        id=7,
        name="Chance",
        monument="Fortune Wheel",
        city="National",
        state="India",
        type=SpaceType.CHANCE,
        description="Draw a Chance Card.",
        icon="clover"
    ),
    BoardSpace(
        id=8,
        name="Calangute Strip",
        monument="Aguada Fort & Beach",
        city="North Goa",
        state="Goa",
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
        description="World-renowned coastal tourist destination and 17th-century Portuguese fort.",
        icon="sun"
    ),
    BoardSpace(
        id=9,
        name="Marine Drive Kochi",
        monument="Chinese Fishing Nets & Fort",
        city="Kochi",
        state="Kerala",
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
        description="Arabian Sea spice trade port and scenic waterfront promenade.",
        icon="anchor"
    ),
    # Left Column: 10 (Jail) to 20 (Free Parking)
    BoardSpace(
        id=10,
        name="In Jail / Just Visiting",
        monument="Central Detention Facility",
        city="Judicial",
        state="Jurisdiction",
        type=SpaceType.JAIL,
        description="Detention Facility. Visiting is free; prisoners must pay ₹500 or roll doubles.",
        icon="shield-alert"
    ),
    BoardSpace(
        id=11,
        name="MI Road (Pink City)",
        monument="Hawa Mahal & City Palace",
        city="Jaipur",
        state="Rajasthan",
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
        description="Royal Pink City handicraft corridor near the Palace of Winds.",
        icon="gem"
    ),
    BoardSpace(
        id=12,
        name="National Power Grid",
        monument="PowerGrid & NTPC",
        city="National",
        state="Infrastructure",
        type=SpaceType.UTILITY,
        price=1500,
        mortgage_value=750,
        description="National Electricity Transmission Grid. Rent: 40x roll (1 owned) or 100x roll (both owned).",
        icon="zap"
    ),
    BoardSpace(
        id=13,
        name="Dashashwamedh Ghat",
        monument="Kashi Vishwanath Corridor",
        city="Varanasi",
        state="Uttar Pradesh",
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
        description="World's oldest spiritual riverfront on the sacred Ganges.",
        icon="flame"
    ),
    BoardSpace(
        id=14,
        name="Mall Road",
        monument="The Ridge & Viceregal Lodge",
        city="Shimla",
        state="Himachal Pradesh",
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
        description="Historic Himalayan hill station ridge and colonial commercial avenue.",
        icon="mountain"
    ),
    BoardSpace(
        id=15,
        name="CSMT Terminus",
        monument="Victoria Gothic Terminus",
        city="Mumbai",
        state="Maharashtra",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        description="UNESCO World Heritage Victorian Gothic railway headquarters of Central Railway.",
        icon="train"
    ),
    BoardSpace(
        id=16,
        name="FC Road (Deccan)",
        monument="Shaniwar Wada Fort",
        city="Pune",
        state="Maharashtra",
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
        description="Historic Maratha empire seat and vibrant modern tech-student district.",
        icon="coffee"
    ),
    BoardSpace(
        id=17,
        name="Community Chest",
        monument="Community Welfare",
        city="National",
        state="India",
        type=SpaceType.COMMUNITY,
        description="Draw a Community Chest Card.",
        icon="users"
    ),
    BoardSpace(
        id=18,
        name="CG Road",
        monument="Sabarmati Riverfront & Ashram",
        city="Ahmedabad",
        state="Gujarat",
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
        description="Major financial high-street and commercial retail boulevard.",
        icon="briefcase"
    ),
    BoardSpace(
        id=19,
        name="Sector 17 Plaza",
        monument="Rock Garden & Capitol Complex",
        city="Chandigarh",
        state="Chandigarh",
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
        description="Le Corbusier planned pedestrian plaza and capital commercial zone.",
        icon="building"
    ),
    # Top Row: 20 (Free Parking) to 30 (Go To Jail)
    BoardSpace(
        id=20,
        name="Free Parking",
        monument="Public Transit Rest Hub",
        city="Safe",
        state="Zone",
        type=SpaceType.FREE_PARKING,
        description="Resting Zone. No rent or fee charged.",
        icon="tent"
    ),
    BoardSpace(
        id=21,
        name="Park Street",
        monument="Victoria Memorial",
        city="Kolkata",
        state="West Bengal",
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
        description="Historic cultural, culinary, and corporate avenue near Victoria Memorial.",
        icon="music"
    ),
    BoardSpace(
        id=22,
        name="Chance",
        monument="Fortune Wheel",
        city="National",
        state="India",
        type=SpaceType.CHANCE,
        description="Draw a Chance Card.",
        icon="clover"
    ),
    BoardSpace(
        id=23,
        name="HITEC City",
        monument="Cyber Towers & Golconda",
        city="Hyderabad",
        state="Telangana",
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
        description="Flagship technology corridor housing leading global tech corporations.",
        icon="cpu"
    ),
    BoardSpace(
        id=24,
        name="Brigade & MG Road",
        monument="Vidhana Soudha & Cubbon Park",
        city="Bengaluru",
        state="Karnataka",
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
        description="Silicon Plateau's bustling commercial downtown and innovation nexus.",
        icon="laptop"
    ),
    BoardSpace(
        id=25,
        name="New Delhi Junction",
        monument="India Gate & Railway Hub",
        city="New Delhi",
        state="Delhi",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        description="Northern Railway mega-terminus connecting the capital across India.",
        icon="train"
    ),
    BoardSpace(
        id=26,
        name="T. Nagar & Anna Salai",
        monument="Ripon Building & Marina Beach",
        city="Chennai",
        state="Tamil Nadu",
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
        description="India's largest retail hub for gold jewellery and silk commerce.",
        icon="shopping-bag"
    ),
    BoardSpace(
        id=27,
        name="Golf Course Road",
        monument="Cyber Hub Towers",
        city="Gurugram",
        state="Haryana",
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
        description="Millennium City's ultra-luxury condominium and corporate glass corridor.",
        icon="building-2"
    ),
    BoardSpace(
        id=28,
        name="National Water Authority",
        monument="Jal Jeevan Infrastructure",
        city="National",
        state="Infrastructure",
        type=SpaceType.UTILITY,
        price=1500,
        mortgage_value=750,
        description="National Water Infrastructure. Rent: 40x roll (1 owned) or 100x roll (both owned).",
        icon="droplets"
    ),
    BoardSpace(
        id=29,
        name="GS Road Dispur",
        monument="Kamakhya Temple & Brahmaputra",
        city="Guwahati",
        state="Assam",
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
        description="Commercial gateway and economic capital of Northeast India.",
        icon="map-pin"
    ),
    # Right Column: 30 (Go to Jail) to 39
    BoardSpace(
        id=30,
        name="Go To Jail",
        monument="Court Warrant",
        city="Legal",
        state="Summons",
        type=SpaceType.GO_TO_JAIL,
        description="Advance directly to Jail. Do not pass GO, do not collect ₹2,000.",
        icon="gavel"
    ),
    BoardSpace(
        id=31,
        name="Connaught Place",
        monument="India Gate & Heritage Colonnade",
        city="New Delhi",
        state="Delhi",
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
        description="Famous Georgian circular colonnade financial and retail powerhouse.",
        icon="compass"
    ),
    BoardSpace(
        id=32,
        name="Bandra-Kurla Complex",
        monument="Bandra-Worli Sea Link & BKC",
        city="Mumbai",
        state="Maharashtra",
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
        description="Premier central financial district housing stock exchanges and conglomerates.",
        icon="landmark"
    ),
    BoardSpace(
        id=33,
        name="Community Chest",
        monument="Community Welfare",
        city="National",
        state="India",
        type=SpaceType.COMMUNITY,
        description="Draw a Community Chest Card.",
        icon="users"
    ),
    BoardSpace(
        id=34,
        name="Lutyens' Bungalow Zone",
        monument="Rashtrapati Bhavan & Qutub Minar",
        city="New Delhi",
        state="Delhi",
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
        description="The nation's most elite diplomatic power seat and sprawling tree-lined estates.",
        icon="crown"
    ),
    BoardSpace(
        id=35,
        name="Chennai Central MGR",
        monument="Romanesque Railway Central",
        city="Chennai",
        state="Tamil Nadu",
        type=SpaceType.TRANSPORT,
        price=2000,
        base_rent=250,
        mortgage_value=1000,
        description="Southern Railway's majestic crimson Romanesque transit nexus.",
        icon="train"
    ),
    BoardSpace(
        id=36,
        name="Chance",
        monument="Fortune Wheel",
        city="National",
        state="India",
        type=SpaceType.CHANCE,
        description="Draw a Chance Card.",
        icon="clover"
    ),
    BoardSpace(
        id=37,
        name="Altamount Road",
        monument="Gateway of India & Antilia",
        city="Mumbai",
        state="Maharashtra",
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
        description="Billionaires' Boulevard on Cumballa Hill, home to India's top magnates.",
        icon="diamond"
    ),
    BoardSpace(
        id=38,
        name="Luxury Tax",
        monument="High-Wealth Cess",
        city="Treasury",
        state="Taxation",
        type=SpaceType.TAX,
        price=1000,
        description="Pay statutory Luxury Tax of ₹1,000 to the Bank.",
        icon="badge-dollar-sign"
    ),
    BoardSpace(
        id=39,
        name="Marine Drive Promenade",
        monument="Queen's Necklace & Gateway",
        city="Mumbai",
        state="Maharashtra",
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
        description="The iconic Queen's Necklace waterfront arc and crown jewel of Indian real estate.",
        icon="sparkle"
    )
]

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
