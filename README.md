# 👑 KUBER — The Great Indian Property Empire
### Full-Stack Indian Monopoly Game (Next.js + FastAPI + WebSockets)

Inspired by classic Monopoly board game dynamics, **Kuber** reimagines the real-estate trading experience through the vibrant lens of Indian cities, cultural landmarks, transportation networks, and economic scenarios.

---

## 🏗️ Architecture

```
MONOPOLY/
├── backend/                  # FastAPI + WebSockets + Python Engine
│   ├── app/
│   │   ├── api/              # REST Endpoints & Real-time WebSockets
│   │   ├── engine/           # Game Engine & Smart AI Bots
│   │   ├── models/           # Board (40 Spaces), Cards (32), State
│   │   └── main.py           # FastAPI Server Entrypoint
│   └── run.py                # Server launcher script
├── frontend/                 # Next.js 16 (Turbopack + Tailwind v4 + Lucide)
│   ├── src/
│   │   ├── app/              # App Router (Landing & Game Room)
│   │   ├── components/       # 40-Space Board, Dice, Modals, HUD
│   │   └── lib/              # Board Data, Web Audio Synthesizer, Types
└── INDIAN_MONOPOLY_BLUEPRINT.md # Master Game Design Blueprint
```

---

## 🚀 How to Run Locally

### 1. Launch FastAPI Backend (Port 8000)

```powershell
cd backend
python run.py
```
> API will run on `http://127.0.0.1:8000` (Swagger docs at `http://127.0.0.1:8000/docs`).

### 2. Launch Next.js Frontend (Port 3000)

```powershell
cd frontend
npm run dev
```
> Open [http://localhost:3000](http://localhost:3000) in your browser to play!

---

## 🎲 Game Features

1. **40 Authentic Indian Spaces:**
   - **22 Properties across 8 Color Groups:** From *Chandni Chowk* (₹600) to *Marine Drive* (₹4,000).
   - **4 Transportation Hubs:** *Howrah Junction*, *CSMT Terminus*, *New Delhi Junction*, *Chennai Central*.
   - **2 Public Utilities:** *National Power Grid* & *Jal Jeevan Board*.
   - **Special Spaces:** *Aarambh (GO)*, *Aaykar (Income Tax)*, *Police Chowki (Jail/Detention)*, *Vishram Sthal (Free Parking)*, *Nyayalay Saman (Go to Chowki)*, *GST Luxury Cess*.
2. **8 Bespoke Metallic Tokens:**
   - Auto-Rickshaw, Royal Elephant, Cricket Bat & Ball, Cutting Chai, WAP-7 Locomotive, Bajaj Chetak Scooter, National Lotus, Bollywood Clapperboard.
3. **Smart AI Tycoons:**
   - Play solo against AI tycoons (*Mukesh Tycoon*, *Rakesh Ji*, *Tech Founder*, *Chaiwala Tycoon*).
4. **Multiplayer Room Codes:**
   - Host private lobbies with room codes (`KUBER-XXXX`) and play with friends in real time over WebSockets.
5. **Interactive Mechanics:**
   - Real-time 3D dice shaker with doubles rules & speeding citations.
   - Public property auctions with live timer and bidding.
   - Construction manager for Bhavans (Houses) & Mahals (Hotels).
   - Title deed certificates with full rent matrices.
   - 32 Kismat (Luck) & Panchayat (Community) cards with custom actions.
   - Built-in Web Audio API sound synthesizer (no external audio assets needed).
