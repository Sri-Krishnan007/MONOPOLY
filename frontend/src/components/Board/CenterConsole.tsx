"use client";

import React, { useState } from "react";
import { GameState, Player, BoardSpace } from "@/lib/types";
import { sounds } from "@/lib/sounds";
import { Dices, Building, Hammer, Shield, ScrollText, CheckCircle2, ChevronRight, Crown } from "lucide-react";

interface CenterConsoleProps {
  game: GameState;
  myPlayerId: string;
  currentSpace?: BoardSpace;
  onRollDice: () => void;
  onBuyProperty: (spaceId: number) => void;
  onDeclineBuy: (spaceId: number) => void;
  onPayBail: () => void;
  onUseJailCard: () => void;
  onEndTurn: () => void;
  onOpenPortfolio: () => void;
}

const DIE_PIPS: Record<number, number[][]> = {
  1: [[1, 1]],
  2: [[0, 0], [2, 2]],
  3: [[0, 0], [1, 1], [2, 2]],
  4: [[0, 0], [0, 2], [2, 0], [2, 2]],
  5: [[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]],
  6: [[0, 0], [0, 2], [1, 0], [1, 2], [2, 0], [2, 2]],
};

export const CenterConsole: React.FC<CenterConsoleProps> = ({
  game,
  myPlayerId,
  currentSpace,
  onRollDice,
  onBuyProperty,
  onDeclineBuy,
  onPayBail,
  onUseJailCard,
  onEndTurn,
  onOpenPortfolio
}) => {
  const [isRolling, setIsRolling] = useState(false);
  const curPlayer = game.players[game.current_player_index];
  const isMyTurn = curPlayer?.id === myPlayerId;
  const isHost = game.host_id === myPlayerId;

  const handleRoll = () => {
    if (!isMyTurn || isRolling) return;
    setIsRolling(true);
    sounds.playDiceRoll();
    setTimeout(() => {
      setIsRolling(false);
      onRollDice();
    }, 600);
  };

  const renderDie = (value: number) => {
    const pips = DIE_PIPS[value] || DIE_PIPS[1];
    return (
      <div
        className={`w-12 h-12 sm:w-14 sm:h-14 bg-gradient-to-br from-amber-50 via-slate-100 to-amber-100 rounded-xl shadow-lg border-2 border-amber-500/80 p-1.5 grid grid-cols-3 grid-rows-3 gap-0.5 transition-transform duration-300 ${
          isRolling ? "animate-spin scale-110" : "hover:scale-105"
        }`}
      >
        {Array.from({ length: 3 }).map((_, r) =>
          Array.from({ length: 3 }).map((_, c) => {
            const hasPip = pips.some(([pr, pc]) => pr === r && pc === c);
            return (
              <div key={`${r}-${c}`} className="flex items-center justify-center">
                {hasPip && (
                  <span className="w-2 h-2 sm:w-2.5 sm:h-2.5 bg-amber-950 rounded-full shadow-inner" />
                )}
              </div>
            );
          })
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center justify-between h-full w-full p-4 text-center bg-gradient-to-b from-slate-950/80 via-slate-900/90 to-slate-950/95 rounded-2xl border border-amber-500/30 backdrop-blur-md shadow-2xl">
      {/* Title & Indian Jaali Header */}
      <div className="w-full">
        <div className="flex items-center justify-center gap-2">
          <Crown className="w-5 h-5 text-amber-400 animate-pulse" />
          <h2 className="text-base sm:text-xl font-black tracking-widest uppercase bg-gradient-to-r from-amber-300 via-yellow-400 to-amber-500 bg-clip-text text-transparent">
            KUBER
          </h2>
          <Crown className="w-5 h-5 text-amber-400 animate-pulse" />
        </div>
        <p className="text-[10px] sm:text-xs text-amber-400/80 tracking-wide font-medium">
          The Great Indian Property Empire • भारत का कुबेर
        </p>
      </div>

      {/* Turn & Status Indicator */}
      <div className="my-2 px-3 py-1.5 rounded-full bg-slate-800/80 border border-slate-700/80 text-xs sm:text-sm text-slate-200 shadow-inner">
        {curPlayer ? (
          <div className="flex items-center gap-2">
            <span
              className="w-2.5 h-2.5 rounded-full animate-ping"
              style={{ backgroundColor: curPlayer.color }}
            />
            <span className="font-semibold text-amber-300">{curPlayer.name}&apos;s Turn</span>
            {curPlayer.in_jail && (
              <span className="text-[10px] bg-red-900/80 text-red-200 px-1.5 py-0.5 rounded">
                In Hawalat ({curPlayer.jail_turns}/3)
              </span>
            )}
          </div>
        ) : (
          <span>Waiting for game to begin...</span>
        )}
      </div>

      {/* 3D Dice Display */}
      <div className="flex items-center justify-center gap-4 my-2">
        {renderDie(game.dice_1 || 1)}
        {renderDie(game.dice_2 || 1)}
      </div>

      {/* Total Dice Value & Doubles Notice */}
      <div className="text-xs text-slate-300">
        <span className="font-bold text-amber-400">Total: {game.dice_1 + game.dice_2}</span>
        {game.dice_1 === game.dice_2 && game.dice_1 > 0 && (
          <span className="ml-2 font-bold text-emerald-400 animate-pulse">✨ DOUBLES!</span>
        )}
      </div>

      {/* Current Action Console */}
      <div className="w-full flex flex-col gap-2 mt-2">
        {/* Phase: In Jail Decision */}
        {isMyTurn && curPlayer?.in_jail && (
          <div className="flex flex-wrap items-center justify-center gap-2">
            {curPlayer.cash >= 500 && (
              <button
                onClick={() => { sounds.playCashChime(); onPayBail(); }}
                className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded-lg text-xs font-bold shadow-md transition-all flex items-center gap-1.5"
              >
                <Shield className="w-3.5 h-3.5" /> Pay ₹500 Bail Fine
              </button>
            )}
            {curPlayer.get_out_of_jail_cards > 0 && (
              <button
                onClick={() => { sounds.playBuyProperty(); onUseJailCard(); }}
                className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold shadow-md transition-all flex items-center gap-1.5"
              >
                <ScrollText className="w-3.5 h-3.5" /> Use Zamanat Patra
              </button>
            )}
          </div>
        )}

        {/* Phase: Pre-Roll */}
        {isMyTurn && (game.turn_phase === "pre_roll" || game.turn_phase === "in_jail_decision") && (
          <button
            onClick={handleRoll}
            disabled={isRolling}
            className="w-full py-2.5 px-4 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-black rounded-xl text-sm shadow-xl shadow-amber-500/20 transform active:scale-95 transition-all flex items-center justify-center gap-2 animate-bounce"
          >
            <Dices className="w-5 h-5" /> ROLL THE SACRED DICE (पासा फेंकें)
          </button>
        )}

        {/* Phase: Buy or Auction Decision */}
        {isMyTurn && game.turn_phase === "buy_or_auction_decision" && currentSpace && (
          <div className="flex flex-col gap-2 p-2 bg-slate-950/80 rounded-xl border border-amber-500/40">
            <p className="text-xs text-slate-200">
              Landed on <strong className="text-amber-300">{currentSpace.name}</strong> for{" "}
              <strong className="text-emerald-400">₹{currentSpace.price.toLocaleString("en-IN")}</strong>
            </p>
            <div className="flex gap-2">
              <button
                onClick={() => { sounds.playBuyProperty(); onBuyProperty(currentSpace.id); }}
                disabled={curPlayer.cash < currentSpace.price}
                className="flex-1 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-bold rounded-lg text-xs transition-all flex items-center justify-center gap-1 shadow-md"
              >
                <Building className="w-3.5 h-3.5" /> Buy for ₹{currentSpace.price.toLocaleString("en-IN")}
              </button>
              <button
                onClick={() => onDeclineBuy(currentSpace.id)}
                className="flex-1 py-2 bg-rose-700 hover:bg-rose-600 text-white font-bold rounded-lg text-xs transition-all flex items-center justify-center gap-1 shadow-md"
              >
                <Hammer className="w-3.5 h-3.5" /> Public Auction
              </button>
            </div>
          </div>
        )}

        {/* Phase: Post-Turn (End Turn & Portfolio) */}
        {isMyTurn && game.turn_phase === "post_turn" && (
          <div className="flex gap-2">
            <button
              onClick={onOpenPortfolio}
              className="flex-1 py-2 bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold rounded-xl text-xs border border-amber-500/40 transition-all flex items-center justify-center gap-1.5"
            >
              <Building className="w-3.5 h-3.5" /> Build & Manage
            </button>
            <button
              onClick={onEndTurn}
              className="flex-1 py-2 bg-gradient-to-r from-amber-600 to-amber-500 hover:from-amber-500 hover:to-amber-400 text-slate-950 font-black rounded-xl text-xs transition-all flex items-center justify-center gap-1.5 shadow-lg shadow-amber-600/20"
            >
              <CheckCircle2 className="w-3.5 h-3.5" /> End Turn <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Not My Turn Banner */}
        {!isMyTurn && curPlayer && (
          <p className="text-xs text-slate-400 italic py-2">
            Waiting for {curPlayer.name} to make their move...
          </p>
        )}
      </div>
    </div>
  );
};
