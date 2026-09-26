"use client";

import React from "react";
import { GameState } from "@/lib/types";
import { PLAYER_TOKENS } from "@/lib/boardData";
import { Wallet, ShieldAlert, Building, Bot } from "lucide-react";

interface PlayerLedgerProps {
  game: GameState;
  myPlayerId: string;
}

export const PlayerLedger: React.FC<PlayerLedgerProps> = ({ game, myPlayerId }) => {
  const getTokenEmoji = (tokenId: string) => {
    const found = PLAYER_TOKENS.find(t => t.id === tokenId);
    return found ? found.icon : "♟️";
  };

  return (
    <div className="flex flex-col gap-2.5 p-3.5 bg-slate-900/90 rounded-2xl border border-slate-800 backdrop-blur-md shadow-xl select-none">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Wallet className="w-4 h-4 text-amber-400" />
          <h3 className="font-bold text-xs sm:text-sm text-slate-100 uppercase tracking-wider">
            Player Ledger
          </h3>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">
          Round {game.turn_number}
        </span>
      </div>

      <div className="flex flex-col gap-1.5">
        {game.players.map((player, idx) => {
          const isCurrentTurn = game.current_player_index === idx && game.status === "playing";
          const isMe = player.id === myPlayerId;
          const propertyCount = Object.values(game.properties).filter(
            (p) => p.owner_id === player.id
          ).length;

          return (
            <div
              key={player.id}
              className={`p-2 rounded-xl border transition-all ${
                isCurrentTurn
                  ? "bg-slate-800/95 border-amber-400 shadow-md shadow-amber-500/10 ring-1 ring-amber-400/50"
                  : "bg-slate-950/60 border-slate-800/80"
              } ${player.is_bankrupt ? "opacity-40 grayscale" : ""}`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div
                    className="w-6 h-6 rounded-full flex items-center justify-center text-xs shadow border border-white/20"
                    style={{ backgroundColor: player.color }}
                  >
                    {getTokenEmoji(player.token)}
                  </div>
                  <div>
                    <div className="flex items-center gap-1">
                      <span className="font-bold text-xs text-slate-100">
                        {player.name}
                      </span>
                      {isMe && (
                        <span className="text-[8px] bg-amber-500/20 text-amber-300 px-1 rounded font-bold">
                          YOU
                        </span>
                      )}
                      {player.is_bot && (
                        <span className="text-[8px] bg-sky-900 text-sky-200 px-1 rounded flex items-center gap-0.5">
                          <Bot className="w-2.5 h-2.5" /> AI
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-2 text-[9px] text-slate-400 mt-0.5">
                      <span className="flex items-center gap-0.5">
                        <Building className="w-2.5 h-2.5 text-slate-500" /> {propertyCount} Deeds
                      </span>
                      {player.in_jail && (
                        <span className="flex items-center gap-0.5 text-rose-400 font-semibold">
                          <ShieldAlert className="w-2.5 h-2.5" /> In Jail
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  {player.is_bankrupt ? (
                    <span className="text-[10px] font-bold text-rose-500">BANKRUPT</span>
                  ) : (
                    <span className="font-black text-xs sm:text-sm text-emerald-400">
                      ₹{player.cash.toLocaleString("en-IN")}
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
