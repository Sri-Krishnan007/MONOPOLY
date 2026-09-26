"use client";

import React from "react";
import { GameState } from "@/lib/types";
import { BOARD_SPACES, COLOR_GROUP_STYLES } from "@/lib/boardData";
import { sounds } from "@/lib/sounds";
import { X, Building, AlertCircle, Plus, ArrowUp } from "lucide-react";

interface PortfolioModalProps {
  game: GameState;
  myPlayerId: string;
  onClose: () => void;
  onBuildBhavan: (spaceId: number) => void;
  onBuildMahal: (spaceId: number) => void;
  onMortgage: (spaceId: number) => void;
  onUnmortgage: (spaceId: number) => void;
}

export const PortfolioModal: React.FC<PortfolioModalProps> = ({
  game,
  myPlayerId,
  onClose,
  onBuildBhavan,
  onBuildMahal,
  onMortgage,
  onUnmortgage
}) => {
  const me = game.players.find(p => p.id === myPlayerId);
  const myProperties = Object.values(game.properties).filter(
    (prop) => prop.owner_id === myPlayerId
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in select-none">
      <div className="relative w-full max-w-2xl max-h-[85vh] flex flex-col p-6 bg-slate-900 border-2 border-amber-500/80 rounded-3xl shadow-2xl text-slate-100 overflow-hidden">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-full bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-all"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Building className="w-6 h-6 text-amber-400" />
            <h2 className="text-xl font-black text-slate-100">
              REAL ESTATE PORTFOLIO & DEVELOPMENT
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Build Houses, upgrade to Hotels, or leverage mortgage credit with the Bank.
          </p>
          <div className="flex items-center justify-between mt-2 p-2 bg-slate-950 rounded-xl border border-slate-800 text-xs">
            <span>
              Cash Reserves: <strong className="text-emerald-400">₹{(me?.cash || 0).toLocaleString("en-IN")}</strong>
            </span>
            <span>
              Bank Supply: <strong className="text-emerald-400">{game.bank_houses} Houses</strong> /{" "}
              <strong className="text-rose-400">{game.bank_hotels} Hotels</strong>
            </span>
          </div>
        </div>

        <div className="flex-grow overflow-y-auto my-4 space-y-3 pr-1">
          {myProperties.length === 0 ? (
            <div className="text-center py-12 text-slate-400">
              <AlertCircle className="w-10 h-10 mx-auto text-amber-500 mb-2" />
              <p className="font-semibold text-sm">You do not own any properties yet!</p>
              <p className="text-xs text-slate-500 mt-1">Roll the dice and acquire properties on your turn.</p>
            </div>
          ) : (
            myProperties.map((prop) => {
              const space = BOARD_SPACES.find(s => s.id === prop.space_id);
              if (!space) return null;
              const colorStyle = space.color_group ? COLOR_GROUP_STYLES[space.color_group] : null;

              return (
                <div
                  key={prop.space_id}
                  className="p-3 bg-slate-950 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3"
                >
                  <div className="flex items-center gap-3">
                    {colorStyle && (
                      <div className={`w-3.5 h-12 rounded-lg ${colorStyle.bg}`} />
                    )}
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-sm text-slate-100">{space.name}</span>
                        {prop.is_mortgaged && (
                          <span className="bg-red-950 text-red-300 border border-red-800 px-1.5 py-0.5 rounded text-[9px] font-bold">
                            MORTGAGED
                          </span>
                        )}
                      </div>
                      <span className="text-xs text-amber-400/90">{space.monument} • {space.city}</span>
                      <div className="flex items-center gap-1.5 mt-1 text-xs text-slate-400">
                        {prop.has_mahal ? (
                          <span className="text-red-400 font-bold flex items-center gap-1">🏨 1 Luxury Hotel</span>
                        ) : prop.bhavans > 0 ? (
                          <span className="text-emerald-400 font-bold flex items-center gap-1">
                            🏠 {prop.bhavans} House(s)
                          </span>
                        ) : (
                          <span>Undeveloped Land</span>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto justify-end">
                    {space.type === "property" && !prop.is_mortgaged && (
                      <>
                        {prop.bhavans < 4 && !prop.has_mahal && (
                          <button
                            onClick={() => { sounds.playBuildBhavan(); onBuildBhavan(prop.space_id); }}
                            className="py-1.5 px-3 bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg text-xs font-bold transition-all flex items-center gap-1 shadow"
                          >
                            <Plus className="w-3.5 h-3.5" /> +1 House (₹{space.house_cost.toLocaleString("en-IN")})
                          </button>
                        )}

                        {prop.bhavans === 4 && !prop.has_mahal && (
                          <button
                            onClick={() => { sounds.playBuyProperty(); onBuildMahal(prop.space_id); }}
                            className="py-1.5 px-3 bg-rose-700 hover:bg-rose-600 text-white rounded-lg text-xs font-bold transition-all flex items-center gap-1 shadow animate-pulse"
                          >
                            <ArrowUp className="w-3.5 h-3.5" /> Hotel (₹{space.hotel_cost.toLocaleString("en-IN")})
                          </button>
                        )}
                      </>
                    )}

                    {prop.is_mortgaged ? (
                      <button
                        onClick={() => { sounds.playCashChime(); onUnmortgage(prop.space_id); }}
                        className="py-1.5 px-3 bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold rounded-lg text-xs transition-all shadow"
                      >
                        Redeem (₹{Math.ceil(space.mortgage_value * 1.1).toLocaleString("en-IN")})
                      </button>
                    ) : (
                      prop.bhavans === 0 && !prop.has_mahal && (
                        <button
                          onClick={() => { sounds.playCashChime(); onMortgage(prop.space_id); }}
                          className="py-1.5 px-3 bg-slate-800 hover:bg-slate-700 text-amber-300 rounded-lg text-xs font-semibold border border-slate-700 transition-all"
                        >
                          Mortgage (+₹{space.mortgage_value.toLocaleString("en-IN")})
                        </button>
                      )
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
