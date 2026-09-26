"use client";

import React from "react";
import { GameCard } from "@/lib/types";
import { Clover, Users, CheckCircle2 } from "lucide-react";

interface CardModalProps {
  card?: GameCard;
  onClose: () => void;
}

export const CardModal: React.FC<CardModalProps> = ({ card, onClose }) => {
  if (!card) return null;

  const isChance = card.deck === "chance";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div
        className={`relative w-full max-w-md p-6 rounded-3xl border-2 shadow-2xl text-center select-none transform transition-all ${
          isChance
            ? "bg-gradient-to-b from-amber-950 via-slate-900 to-amber-950 border-amber-500/80 shadow-amber-500/20"
            : "bg-gradient-to-b from-blue-950 via-slate-900 to-blue-950 border-blue-400/80 shadow-blue-500/20"
        }`}
      >
        <div className="flex justify-center mb-3">
          <div
            className={`p-3 rounded-2xl border ${
              isChance
                ? "bg-amber-500/20 border-amber-400 text-amber-300"
                : "bg-blue-500/20 border-blue-400 text-blue-300"
            }`}
          >
            {isChance ? <Clover className="w-8 h-8 animate-bounce" /> : <Users className="w-8 h-8 animate-bounce" />}
          </div>
        </div>

        <span
          className={`text-xs font-bold uppercase tracking-widest px-3 py-1 rounded-full border ${
            isChance
              ? "bg-amber-900/60 border-amber-600 text-amber-200"
              : "bg-blue-900/60 border-blue-600 text-blue-200"
          }`}
        >
          {isChance ? "CHANCE CARD" : "COMMUNITY CHEST CARD"}
        </span>

        <h3 className="text-xl sm:text-2xl font-black text-slate-100 mt-4 mb-3">
          {card.title}
        </h3>

        <div className="p-4 bg-slate-950/80 rounded-2xl border border-slate-800 text-slate-200 text-sm sm:text-base leading-relaxed mb-6 font-medium shadow-inner">
          {card.description}
        </div>

        <button
          onClick={onClose}
          className={`w-full py-3 px-4 font-black rounded-xl text-slate-950 text-sm shadow-lg transform active:scale-95 transition-all flex items-center justify-center gap-2 ${
            isChance
              ? "bg-gradient-to-r from-amber-400 to-yellow-500 hover:from-amber-300 hover:to-yellow-400"
              : "bg-gradient-to-r from-sky-400 to-blue-500 hover:from-sky-300 hover:to-blue-400 text-white"
          }`}
        >
          <CheckCircle2 className="w-5 h-5" /> Accept & Continue
        </button>
      </div>
    </div>
  );
};
