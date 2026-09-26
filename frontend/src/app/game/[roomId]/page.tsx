"use client";

import React, { useEffect, useState, useRef } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { GameState, GameCard } from "@/lib/types";
import { BOARD_SPACES } from "@/lib/boardData";
import { MonopolyBoard } from "@/components/Board/MonopolyBoard";
import { PlayerLedger } from "@/components/HUD/PlayerLedger";
import { GameLogs } from "@/components/HUD/GameLogs";
import { PropertyRack } from "@/components/HUD/PropertyRack";
import { CityExplorerModal } from "@/components/HUD/CityExplorerModal";
import { LobbyRoom } from "@/components/Lobby/LobbyRoom";
import { CardModal } from "@/components/Modals/CardModal";
import { AuctionModal } from "@/components/Modals/AuctionModal";
import { DeedModal } from "@/components/Modals/DeedModal";
import { PortfolioModal } from "@/components/Modals/PortfolioModal";
import { VictoryModal } from "@/components/Modals/VictoryModal";
import { RulebookModal } from "@/components/HUD/RulebookModal";
import { Crown, BookOpen, Map, Home as HomeIcon } from "lucide-react";

export default function GameRoomPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const roomId = params?.roomId as string;
  const playerId = searchParams.get("playerId") || "";

  const [game, setGame] = useState<GameState | null>(null);
  const [inspectedSpaceId, setInspectedSpaceId] = useState<number | null>(null);
  const [showPortfolio, setShowPortfolio] = useState(false);
  const [showRulebook, setShowRulebook] = useState(false);
  const [showExplorer, setShowExplorer] = useState(false);

  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!roomId || !playerId) return;

    let wsUrl = "";
    if (process.env.NEXT_PUBLIC_WS_URL) {
      const baseWs = process.env.NEXT_PUBLIC_WS_URL.replace(/\/$/, "");
      wsUrl = `${baseWs}/ws/${roomId}/${playerId}`;
    } else if (process.env.NEXT_PUBLIC_API_URL) {
      const baseHttp = process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "");
      const baseWs = baseHttp.replace(/^http/, "ws");
      wsUrl = `${baseWs}/ws/${roomId}/${playerId}`;
    } else {
      const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
      wsUrl = `${protocol}//${window.location.hostname}:8000/ws/${roomId}/${playerId}`;
    }

    const ws = new WebSocket(wsUrl);
    socketRef.current = ws;

    ws.onopen = () => {
      console.log("WebSocket connected to Monopoly server.");
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "GAME_STATE_UPDATE" && data.game) {
          setGame(data.game);
        }
      } catch (err) {
        console.error("Failed to parse WebSocket message", err);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected.");
    };

    return () => {
      ws.close();
    };
  }, [roomId, playerId]);

  const sendAction = (type: string, payload: Record<string, unknown> = {}) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ type, payload }));
    }
  };

  if (!game) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-slate-950 text-slate-100 p-4">
        <Crown className="w-12 h-12 text-amber-400 animate-bounce mb-4" />
        <h2 className="text-xl font-black text-amber-300">ENTERING THE GAME...</h2>
        <p className="text-xs text-slate-400 mt-1">Connecting to live game room...</p>
      </div>
    );
  }

  const inspectedSpace = inspectedSpaceId !== null ? BOARD_SPACES.find(s => s.id === inspectedSpaceId) : undefined;
  const inspectedOwnership = inspectedSpaceId !== null ? game.properties[inspectedSpaceId] : undefined;
  const inspectedOwner = inspectedOwnership ? game.players.find(p => p.id === inspectedOwnership.owner_id) : undefined;
  const winnerPlayer = game.winner_id ? game.players.find(p => p.id === game.winner_id) : undefined;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-amber-950/40 text-slate-100 p-2 sm:p-4 flex flex-col justify-between">
      {/* Top Header */}
      <header className="flex items-center justify-between py-1.5 px-4 bg-slate-900/80 border border-slate-800 rounded-2xl backdrop-blur-md shadow-xl mb-3 select-none">
        <div
          onClick={() => router.push("/")}
          className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity"
        >
          <Crown className="w-5 h-5 text-amber-400" />
          <div>
            <h1 className="text-sm sm:text-base font-black tracking-widest bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-500 bg-clip-text text-transparent uppercase">
              INDIAN MONOPOLY
            </h1>
            <span className="text-[8px] text-amber-400/70 block leading-none">
              Cities & Monuments Edition
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3">
          <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-slate-950 rounded-xl border border-slate-800 text-xs">
            <span className="text-slate-400">Room:</span>
            <span className="font-mono font-bold text-amber-400">{game.room_code}</span>
          </div>

          <button
            onClick={() => setShowExplorer(true)}
            className="py-1 px-3 bg-slate-800 hover:bg-slate-700 text-amber-300 rounded-xl text-xs font-semibold flex items-center gap-1.5 border border-amber-500/30 transition-all"
          >
            <Map className="w-3.5 h-3.5 text-amber-400" /> All Cities (22)
          </button>

          <button
            onClick={() => setShowRulebook(true)}
            className="py-1 px-3 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl text-xs font-semibold flex items-center gap-1.5 border border-slate-700 transition-all"
          >
            <BookOpen className="w-3.5 h-3.5 text-amber-400" /> Rules & Victory
          </button>

          <button
            onClick={() => router.push("/")}
            className="p-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl transition-all"
            title="Leave Game"
          >
            <HomeIcon className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Main Board & HUD Interface */}
      {game.status === "lobby" ? (
        <LobbyRoom
          game={game}
          myPlayerId={playerId}
          onAddBot={() => sendAction("ADD_BOT")}
          onStartGame={() => sendAction("START_GAME")}
        />
      ) : (
        <main className="flex flex-col gap-3 max-w-[1450px] mx-auto w-full">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-3 items-start w-full">
            {/* Left HUD: Player Ledger */}
            <aside className="lg:col-span-3 order-2 lg:order-1">
              <PlayerLedger
                game={game}
                myPlayerId={playerId}
                onOpenExplorer={() => setShowExplorer(true)}
              />
            </aside>

            {/* Center: 40-Space Monopoly Board */}
            <section className="lg:col-span-6 order-1 lg:order-2 flex justify-center">
              <MonopolyBoard
                game={game}
                myPlayerId={playerId}
                onInspectSpace={(spaceId) => setInspectedSpaceId(spaceId)}
                onRollDice={() => sendAction("ROLL_DICE")}
                onBuyProperty={(spaceId) => sendAction("BUY_PROPERTY", { space_id: spaceId })}
                onDeclineBuy={(spaceId) => sendAction("DECLINE_BUY", { space_id: spaceId })}
                onPayBail={() => sendAction("PAY_JAIL_BAIL")}
                onUseJailCard={() => sendAction("USE_JAIL_CARD")}
                onEndTurn={() => sendAction("END_TURN")}
                onOpenPortfolio={() => setShowPortfolio(true)}
              />
            </section>

            {/* Right HUD: Activity Stream */}
            <aside className="lg:col-span-3 order-3">
              <GameLogs logs={game.logs} />
            </aside>
          </div>

          {/* Bottom Property Rack: What You Bought */}
          <PropertyRack
            game={game}
            myPlayerId={playerId}
            onInspectSpace={(spaceId) => setInspectedSpaceId(spaceId)}
            onBuildHouse={(spaceId) => sendAction("BUILD_BHAVAN", { space_id: spaceId })}
            onBuildHotel={(spaceId) => sendAction("BUILD_MAHAL", { space_id: spaceId })}
          />
        </main>
      )}

      {/* Footer Branding */}
      <footer className="mt-2 text-center text-[10px] text-slate-500 py-1">
        Indian Monopoly: Cities & Monuments • Official Hasbro Rules & Victory Mechanics
      </footer>

      {/* Overlays and Modals */}
      {game.last_drawn_card && game.turn_phase === "card_drawn" && (
        <CardModal
          card={game.last_drawn_card as GameCard}
          onClose={() => sendAction("END_TURN")}
        />
      )}

      {game.active_auction && game.turn_phase === "auction_in_progress" && (
        <AuctionModal
          auction={game.active_auction}
          players={game.players}
          myPlayerId={playerId}
          onPlaceBid={(amount) => sendAction("PLACE_BID", { amount })}
          onConcludeAuction={() => sendAction("CONCLUDE_AUCTION")}
        />
      )}

      {inspectedSpace && (
        <DeedModal
          space={inspectedSpace}
          ownership={inspectedOwnership}
          owner={inspectedOwner}
          onClose={() => setInspectedSpaceId(null)}
        />
      )}

      {showPortfolio && (
        <PortfolioModal
          game={game}
          myPlayerId={playerId}
          onClose={() => setShowPortfolio(false)}
          onBuildBhavan={(spaceId) => sendAction("BUILD_BHAVAN", { space_id: spaceId })}
          onBuildMahal={(spaceId) => sendAction("BUILD_MAHAL", { space_id: spaceId })}
          onMortgage={(spaceId) => sendAction("MORTGAGE_PROPERTY", { space_id: spaceId })}
          onUnmortgage={(spaceId) => sendAction("UNMORTGAGE_PROPERTY", { space_id: spaceId })}
        />
      )}

      {showExplorer && (
        <CityExplorerModal
          game={game}
          onInspectSpace={(spaceId) => { setInspectedSpaceId(spaceId); }}
          onClose={() => setShowExplorer(false)}
        />
      )}

      {showRulebook && (
        <RulebookModal onClose={() => setShowRulebook(false)} />
      )}

      {game.status === "completed" && (
        <VictoryModal
          winner={winnerPlayer}
          onPlayAgain={() => router.push("/")}
        />
      )}
    </div>
  );
}
