"use client";

import React, { useState } from "react";
import { GameState, PlayerTokenInfo } from "@/lib/types";
import { PLAYER_TOKENS } from "@/lib/boardData";
import { sounds } from "@/lib/sounds";
import { Crown, Users, Bot, Play, Copy, Check } from "lucide-react";

interface LobbyRoomProps {
  game: GameState;
  myPlayerId: string;
  onAddBot: () => void;
  onStartGame: () => void;
}

export const LobbyRoom: React.FC<LobbyRoomProps> = ({
  game,
  myPlayerId,
  onAddBot,
  onStartGame
}) => {
  const [copied, setCopied] = useState(false);
  const isHost = game.host_id === myPlayerId;

  const copyRoomCode = () => {
    navigator.clipboard.writeText(game.room_code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getTokenInfo = (tokenId: string): PlayerTokenInfo | undefined => {
    return PLAYER_TOKENS.find(t => t.id === tokenId);
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-6 sm:p-8 bg-slate-900/90 border-2 border-amber-500/80 rounded-3xl shadow-2xl backdrop-blur-md text-slate-100 select-none">
      <div className="text-center pb-5 border-b border-slate-800">
        <div className="flex items-center justify-center gap-2 mb-1">
          <Crown className="w-6 h-6 text-amber-400 animate-pulse" />
          <h1 className="text-2xl sm:text-3xl font-black bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-500 bg-clip-text text-transparent uppercase tracking-wider">
            GAME LOBBY
          </h1>
          <Crown className="w-6 h-6 text-amber-400 animate-pulse" />
        </div>
        <p className="text-xs text-amber-400/80 font-medium">
          Indian Monopoly: Cities & Monuments Edition
        </p>

        <div className="mt-4 inline-flex items-center gap-3 px-4 py-2 bg-slate-950 rounded-2xl border border-amber-500/40 shadow-inner">
          <span className="text-xs text-slate-400 font-medium">Room Code:</span>
          <span className="font-mono text-base sm:text-lg font-black text-amber-400 tracking-widest">
            {game.room_code}
          </span>
          <button
            onClick={copyRoomCode}
            className="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-all flex items-center gap-1 text-xs"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? "Copied!" : "Copy"}
          </button>
        </div>
      </div>

      <div className="my-6">
        <div className="flex items-center justify-between mb-3">
          <h3 className="font-bold text-xs sm:text-sm text-slate-200 flex items-center gap-1.5">
            <Users className="w-4 h-4 text-amber-400" /> Connected Players ({game.players.length}/8)
          </h3>
          {isHost && game.players.length < 8 && (
            <button
              onClick={() => { sounds.playBuyProperty(); onAddBot(); }}
              className="py-1.5 px-3 bg-sky-900/80 hover:bg-sky-800 text-sky-200 text-xs font-bold rounded-xl border border-sky-600/50 transition-all flex items-center gap-1.5 shadow"
            >
              <Bot className="w-3.5 h-3.5" /> + Add AI Bot
            </button>
          )}
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          {game.players.map((p) => {
            const tokenInfo = getTokenInfo(p.token);
            const isMe = p.id === myPlayerId;

            return (
              <div
                key={p.id}
                className="p-3 bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div
                    className="w-9 h-9 rounded-2xl flex items-center justify-center text-lg shadow border border-white/20"
                    style={{ backgroundColor: p.color }}
                  >
                    {tokenInfo?.icon || "♟️"}
                  </div>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <span className="font-bold text-sm text-slate-100">{p.name}</span>
                      {isMe && (
                        <span className="text-[8px] bg-amber-500/20 text-amber-300 px-1 rounded font-bold">
                          YOU
                        </span>
                      )}
                      {p.id === game.host_id && (
                        <span className="text-[8px] bg-amber-600 text-white px-1 rounded font-bold">
                          HOST
                        </span>
                      )}
                      {p.is_bot && (
                        <span className="text-[8px] bg-sky-950 text-sky-300 border border-sky-800 px-1 rounded font-bold">
                          AI
                        </span>
                      )}
                    </div>
                    <span className="text-xs text-slate-400">{tokenInfo?.name} ({tokenInfo?.finish})</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="pt-4 border-t border-slate-800 flex flex-col gap-2">
        {isHost ? (
          <button
            onClick={() => { sounds.playCashChime(); onStartGame(); }}
            disabled={game.players.length < 2}
            className="w-full py-3.5 px-6 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-600 hover:from-amber-400 hover:to-yellow-400 disabled:opacity-40 text-slate-950 font-black text-sm rounded-2xl shadow-xl shadow-amber-500/20 transform active:scale-95 transition-all flex items-center justify-center gap-2"
          >
            <Play className="w-4 h-4 fill-current" />
            {game.players.length < 2
              ? "Need at least 2 players to start"
              : "START GAME"}
          </button>
        ) : (
          <div className="p-3.5 bg-slate-950/80 rounded-2xl border border-slate-800 text-center text-xs text-slate-400">
            Waiting for the host to start the game...
          </div>
        )}
      </div>
    </div>
  );
};
