"use client";

import React from "react";
import { GameState, PropertyOwnership } from "@/lib/types";
import { BOARD_SPACES, COLOR_GROUP_STYLES } from "@/lib/boardData";
import { sounds } from "@/lib/sounds";
import { Building, Plus, ArrowUp, Landmark, ShieldCheck, Sparkles } from "lucide-react";

interface PropertyRackProps {
  game: GameState;
  myPlayerId: string;
  onInspectSpace: (spaceId: number) => void;
  onBuildHouse: (spaceId: number) => void;
  onBuildHotel: (spaceId: number) => void;
}

export const PropertyRack: React.FC<PropertyRackProps> = ({
  game,
  myPlayerId,
  onInspectSpace,
  onBuildHouse,
  onBuildHotel
}) => {
  const me = game.players.find(p => p.id === myPlayerId);
  const myProperties = Object.values(game.properties).filter(
    (p) => p.owner_id === myPlayerId
  );

  const isMyTurn = game.players[game.current_player_index]?.id === myPlayerId;

  // Group properties by color
  const colorGroups = ["Brown", "LightBlue", "Pink", "Orange", "Red", "Yellow", "Green", "DarkBlue"];

  return (
    <div className="w-full p-3 bg-slate-900/90 rounded-2xl border border-slate-800 shadow-xl select-none">
      <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Landmark className="w-4 h-4 text-amber-400" />
          <h3 className="font-bold text-xs sm:text-sm text-slate-100 uppercase tracking-wider">
            My Purchased Properties ({myProperties.length} Deeds Owned)
          </h3>
        </div>
        <span className="text-[11px] text-amber-400 font-semibold">
          {me?.name}
        </span>
      </div>

      {myProperties.length === 0 ? (
        <div className="py-4 text-center text-xs text-slate-500 italic">
          You haven&apos;t purchased any properties yet. Roll the dice to acquire Indian cities and landmarks!
        </div>
      ) : (
        <div className="flex gap-2 overflow-x-auto pb-1.5 scrollbar-thin scrollbar-thumb-slate-700">
          {myProperties.map((prop) => {
            const space = BOARD_SPACES.find(s => s.id === prop.space_id);
            if (!space) return null;
            const colorStyle = space.color_group ? COLOR_GROUP_STYLES[space.color_group] : null;

            return (
              <div
                key={prop.space_id}
                onClick={() => onInspectSpace(prop.space_id)}
                className="flex-shrink-0 w-36 sm:w-40 p-2 bg-slate-950 rounded-xl border border-slate-800 hover:border-amber-400 cursor-pointer transition-all flex flex-col justify-between shadow"
              >
                {/* Color Header */}
                {colorStyle ? (
                  <div className={`h-2.5 w-full rounded-md mb-1.5 ${colorStyle.bg} flex items-center justify-end px-1`}>
                    {prop.has_mahal ? (
                      <span className="text-[6px] text-white font-black bg-red-700 px-0.5 rounded">HOTEL</span>
                    ) : prop.bhavans > 0 ? (
                      <span className="text-[7px] text-emerald-300 font-bold">🏠 {prop.bhavans}</span>
                    ) : null}
                  </div>
                ) : (
                  <div className="h-2.5 w-full bg-slate-800 rounded-md mb-1.5" />
                )}

                <div>
                  <h4 className="font-black text-xs text-slate-100 truncate">{space.name}</h4>
                  <p className="text-[9px] text-amber-400/90 truncate font-semibold">{space.monument}</p>
                </div>

                <div className="mt-1.5 pt-1.5 border-t border-slate-800/80 flex items-center justify-between text-[10px]">
                  <span className="text-slate-400">
                    {prop.is_mortgaged ? (
                      <span className="text-red-400 font-bold">Mortgaged</span>
                    ) : prop.has_mahal ? (
                      <span className="text-red-300 font-semibold">Rent: ₹{space.rent_hotel.toLocaleString("en-IN")}</span>
                    ) : prop.bhavans === 1 ? (
                      <span className="text-emerald-300 font-semibold">Rent: ₹{space.rent_1_house.toLocaleString("en-IN")}</span>
                    ) : prop.bhavans === 2 ? (
                      <span className="text-emerald-300 font-semibold">Rent: ₹{space.rent_2_house.toLocaleString("en-IN")}</span>
                    ) : prop.bhavans === 3 ? (
                      <span className="text-emerald-300 font-semibold">Rent: ₹{space.rent_3_house.toLocaleString("en-IN")}</span>
                    ) : prop.bhavans === 4 ? (
                      <span className="text-emerald-300 font-semibold">Rent: ₹{space.rent_4_house.toLocaleString("en-IN")}</span>
                    ) : (
                      <span className="text-slate-300">Base: ₹{space.base_rent}</span>
                    )}
                  </span>

                  {/* Quick Build Action */}
                  {isMyTurn && !prop.is_mortgaged && space.type === "property" && (
                    <div onClick={(e) => e.stopPropagation()}>
                      {prop.bhavans < 4 && !prop.has_mahal && (
                        <button
                          onClick={() => { sounds.playBuildBhavan(); onBuildHouse(prop.space_id); }}
                          title={`Build House for ₹${space.house_cost}`}
                          className="p-1 bg-emerald-700 hover:bg-emerald-600 text-white rounded text-[9px] font-bold"
                        >
                          <Plus className="w-3 h-3" />
                        </button>
                      )}
                      {prop.bhavans === 4 && !prop.has_mahal && (
                        <button
                          onClick={() => { sounds.playBuyProperty(); onBuildHotel(prop.space_id); }}
                          title={`Upgrade to Hotel for ₹${space.hotel_cost}`}
                          className="p-1 bg-rose-700 hover:bg-rose-600 text-white rounded text-[9px] font-bold animate-pulse"
                        >
                          <ArrowUp className="w-3 h-3" />
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
