"use client";

import React from "react";
import { X, BookOpen, Crown, Dices, Shield, Building2, Coins } from "lucide-react";

interface RulebookModalProps {
  onClose: () => void;
}

export const RulebookModal: React.FC<RulebookModalProps> = ({ onClose }) => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-sm animate-fade-in select-none">
      <div className="relative w-full max-w-2xl max-h-[85vh] flex flex-col p-6 bg-slate-900 border-2 border-amber-500/80 rounded-3xl shadow-2xl text-slate-100 overflow-hidden">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-full bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-all"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-amber-400" />
            <h2 className="text-xl font-black text-amber-300 uppercase tracking-wider">
              OFFICIAL MONOPOLY RULEBOOK (HASBRO COMPLIANT)
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Standard property-trading rules adapted with Indian cities, monuments, and transportation hubs.
          </p>
        </div>

        <div className="flex-grow overflow-y-auto my-4 space-y-4 pr-2 text-xs leading-relaxed text-slate-300">
          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Coins className="w-4 h-4" /> 1. Starting Money & Passing GO
            </h4>
            <p>
              Each player starts with exactly <strong>₹15,000</strong> in cash. Whenever a player lands on or passes <strong>START / GO</strong>, the Bank pays them a <strong>₹2,000 salary</strong>.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Dices className="w-4 h-4" /> 2. Movement, Doubles, and Speeding Rule
            </h4>
            <p>
              Roll two 6-sided dice to move clockwise. Rolling doubles gives you an immediate extra turn. If you roll <strong>three consecutive doubles in one turn</strong>, you are caught speeding and sent directly to Jail!
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Building2 className="w-4 h-4" /> 3. Buying, Auctions, and Building
            </h4>
            <p>
              Landing on an unowned property lets you buy it at listed Bank price. If you decline, it is immediately auctioned to all players starting at ₹100. Owning all properties in a color group doubles unimproved rent, and unlocks building up to 4 Houses and 1 Hotel following the <strong>Uniform Building Rule</strong>.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Shield className="w-4 h-4" /> 4. Jail Rules
            </h4>
            <p>
              Get out of Jail by: (a) Rolling doubles on your turn, (b) Paying a ₹500 fine before rolling, or (c) Playing a <em>Get Out of Jail Free</em> card. If doubles are not rolled by turn 3, you must pay ₹500 and advance.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Crown className="w-4 h-4" /> 5. Bankruptcy & Winning
            </h4>
            <p>
              If a player owes more money than their total liquidated assets, they must declare bankruptcy and are eliminated. The last remaining solvent player wins the game!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
