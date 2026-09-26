"use client";

import React, { useEffect } from "react";
import { Player } from "@/lib/types";
import { sounds } from "@/lib/sounds";
import confetti from "canvas-confetti";
import { Trophy, Sparkles, Crown, RotateCcw } from "lucide-react";

interface VictoryModalProps {
  winner?: Player;
  onPlayAgain: () => void;
}

export const VictoryModal: React.FC<VictoryModalProps> = ({ winner, onPlayAgain }) => {
  useEffect(() => {
    sounds.playVictory();
    const duration = 4 * 1000;
    const animationEnd = Date.now() + duration;

    const frame = () => {
      confetti({
        particleCount: 4,
        angle: 60,
        spread: 55,
        origin: { x: 0 },
        colors: ["#F59E0B", "#10B981", "#EF4444", "#3B82F6", "#8B5CF6"]
      });
      confetti({
        particleCount: 4,
        angle: 120,
        spread: 55,
        origin: { x: 1 },
        colors: ["#F59E0B", "#10B981", "#EF4444", "#3B82F6", "#8B5CF6"]
      });

      if (Date.now() < animationEnd) {
        requestAnimationFrame(frame);
      }
    };
    frame();
  }, []);

  if (!winner) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-md animate-fade-in select-none">
      <div className="relative w-full max-w-lg p-8 bg-gradient-to-b from-amber-950 via-slate-900 to-amber-950 border-4 border-amber-500 rounded-3xl shadow-2xl text-center text-slate-100">
        <div className="flex justify-center mb-4">
          <div className="p-4 bg-amber-500/20 border-2 border-amber-400 rounded-full animate-bounce">
            <Trophy className="w-16 h-16 text-amber-400" />
          </div>
        </div>

        <span className="text-xs font-black uppercase tracking-widest text-amber-400">
          SUPREME EMPEROR OF BHARAT • भारत का कुबेर
        </span>

        <h1 className="text-3xl sm:text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-yellow-400 to-amber-300 mt-2 mb-1">
          {winner.name}
        </h1>

        <p className="text-sm font-semibold text-amber-300/80 mb-6">
          Has conquered all rivals and accumulated India&apos;s greatest real estate empire!
        </p>

        <div className="p-4 bg-slate-950/80 rounded-2xl border border-amber-500/40 mb-6">
          <span className="text-xs text-slate-400 block mb-1">Final Wealth</span>
          <span className="text-3xl font-black text-emerald-400">
            ₹{winner.cash.toLocaleString("en-IN")}
          </span>
        </div>

        <button
          onClick={onPlayAgain}
          className="w-full py-3.5 px-6 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-600 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-black rounded-xl text-sm shadow-xl transform active:scale-95 transition-all flex items-center justify-center gap-2"
        >
          <RotateCcw className="w-5 h-5" /> Start New Dynasty (नया खेल)
        </button>
      </div>
    </div>
  );
};
