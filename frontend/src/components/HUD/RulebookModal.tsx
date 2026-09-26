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
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-full bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-all"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Header */}
        <div className="pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-amber-400" />
            <h2 className="text-xl font-black text-amber-300 uppercase tracking-wider">
              KUBER: OFFICIAL GAME COMPENDIUM (नियम पुस्तिका)
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Master the ancient and modern arts of Indian property trading and empire building.
          </p>
        </div>

        {/* Rules Content */}
        <div className="flex-grow overflow-y-auto my-4 space-y-4 pr-2 text-xs leading-relaxed text-slate-300">
          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Coins className="w-4 h-4" /> 1. The ₹15,000 Starting Economy
            </h4>
            <p>
              Each player starts with ₹15,000 in cash. Passing or landing on <strong>Aarambh (GO)</strong> awards a ₹2,000 seasonal dividend.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Dices className="w-4 h-4" /> 2. Dice Rolls & Speeding Rule
            </h4>
            <p>
              Roll 2 six-sided dice to advance clockwise. Rolling doubles gives you an immediate extra turn! However, rolling <strong>three consecutive doubles</strong> triggers an immediate arrest warrant: you are sent directly to Police Chowki!
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Building2 className="w-4 h-4" /> 3. Monopolies & Construction (Bhavans & Mahals)
            </h4>
            <p>
              Acquiring all properties of a single color group doubles their unimproved base rent. Once a full color group is held, you can build <strong>Bhavans</strong> (up to 4 per property) following the Uniform Building Rule, and upgrade 4 Bhavans to a luxury <strong>Mahal</strong>!
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Shield className="w-4 h-4" /> 4. Police Chowki & Hawalat Detention
            </h4>
            <p>
              Escape detention by: (a) Rolling doubles on your turn, (b) Paying a ₹500 legal bail fine before rolling, or (c) Playing a <em>Zamanat Patra</em> (Bail Bond) card. If doubles are not rolled after 3 turns, you must pay ₹500 and advance.
            </p>
          </div>

          <div className="p-3 bg-slate-950 rounded-2xl border border-slate-800">
            <h4 className="font-bold text-amber-400 flex items-center gap-1.5 text-sm mb-1">
              <Crown className="w-4 h-4" /> 5. Winning the Crown of Kuber
            </h4>
            <p>
              Drive all opposing tycoons into financial bankruptcy. The last standing magnate is crowned the supreme <strong>Kuber of India</strong>!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
