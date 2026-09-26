"use client";

import React, { useState } from "react";
import { GameState } from "@/lib/types";
import { BOARD_SPACES, COLOR_GROUP_STYLES } from "@/lib/boardData";
import { X, MapPin, Landmark, Search, ShieldCheck } from "lucide-react";

interface CityExplorerModalProps {
  game: GameState;
  onInspectSpace: (spaceId: number) => void;
  onClose: () => void;
}

export const CityExplorerModal: React.FC<CityExplorerModalProps> = ({
  game,
  onInspectSpace,
  onClose
}) => {
  const [search, setSearch] = useState("");
  const [selectedGroup, setSelectedGroup] = useState<string>("all");

  const groups = [
    { id: "all", label: "All Properties" },
    { id: "Brown", label: "Brown (Delhi / Hyderabad)" },
    { id: "LightBlue", label: "Light Blue (Puducherry / Goa / Kochi)" },
    { id: "Pink", label: "Pink (Jaipur / Varanasi / Shimla)" },
    { id: "Orange", label: "Orange (Pune / Ahmedabad / Chandigarh)" },
    { id: "Red", label: "Red (Kolkata / Hyderabad / Bengaluru)" },
    { id: "Yellow", label: "Yellow (Chennai / Gurugram / Guwahati)" },
    { id: "Green", label: "Green (New Delhi / Mumbai BKC)" },
    { id: "DarkBlue", label: "Dark Blue (Mumbai Prime)" },
    { id: "transport", label: "Railway Hubs (4)" },
    { id: "utility", label: "Utilities (2)" },
  ];

  const filteredSpaces = BOARD_SPACES.filter((space) => {
    if (space.price === 0) return false; // Filter non-purchasable spaces
    if (selectedGroup !== "all") {
      if (selectedGroup === "transport" && space.type !== "transport") return false;
      if (selectedGroup === "utility" && space.type !== "utility") return false;
      if (selectedGroup !== "transport" && selectedGroup !== "utility" && space.color_group !== selectedGroup) return false;
    }
    if (search.trim()) {
      const q = search.toLowerCase();
      return (
        space.name.toLowerCase().includes(q) ||
        space.city.toLowerCase().includes(q) ||
        space.monument.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const getOwner = (spaceId: number) => {
    const ownership = game.properties[spaceId];
    if (!ownership) return null;
    return game.players.find(p => p.id === ownership.owner_id);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in select-none">
      <div className="relative w-full max-w-4xl max-h-[85vh] flex flex-col p-6 bg-slate-900 border-2 border-amber-500/80 rounded-3xl shadow-2xl text-slate-100 overflow-hidden">
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
            <Landmark className="w-6 h-6 text-amber-400" />
            <h2 className="text-xl font-black text-amber-300 uppercase tracking-wider">
              INDIAN CITIES & MONUMENTS DIRECTORY
            </h2>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Browse all 22 Indian cities, famous monuments, transportation gateways, and live ownership statuses.
          </p>

          {/* Search & Filter bar */}
          <div className="flex flex-col sm:flex-row items-center gap-2 mt-3">
            <div className="relative flex-grow w-full">
              <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search city, monument, or state..."
                className="w-full pl-9 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-amber-400"
              />
            </div>

            <select
              value={selectedGroup}
              onChange={(e) => setSelectedGroup(e.target.value)}
              className="w-full sm:w-auto px-3 py-2 bg-slate-950 border border-slate-700 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-amber-400"
            >
              {groups.map((g) => (
                <option key={g.id} value={g.id}>
                  {g.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Directory Grid */}
        <div className="flex-grow overflow-y-auto my-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 pr-1">
          {filteredSpaces.map((space) => {
            const owner = getOwner(space.id);
            const ownership = game.properties[space.id];
            const colorStyle = space.color_group ? COLOR_GROUP_STYLES[space.color_group] : null;

            return (
              <div
                key={space.id}
                onClick={() => { onInspectSpace(space.id); }}
                className="p-3 bg-slate-950 rounded-2xl border border-slate-800 hover:border-amber-400 cursor-pointer transition-all flex flex-col justify-between shadow"
              >
                <div>
                  {colorStyle ? (
                    <div className={`h-2.5 w-full rounded-md mb-2 ${colorStyle.bg}`} />
                  ) : (
                    <div className="h-2.5 w-full bg-slate-800 rounded-md mb-2" />
                  )}

                  <div className="flex items-start justify-between gap-1">
                    <div>
                      <h4 className="font-black text-sm text-slate-100">{space.name}</h4>
                      <p className="text-xs text-amber-400 font-semibold">{space.monument}</p>
                      <p className="text-[10px] text-slate-400">{space.city}, {space.state}</p>
                    </div>
                    <span className="text-xs font-black text-emerald-400">
                      ₹{space.price.toLocaleString("en-IN")}
                    </span>
                  </div>
                </div>

                <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-xs">
                  <span className="text-slate-400">Status:</span>
                  {owner ? (
                    <span
                      className="px-2 py-0.5 rounded text-[10px] font-bold text-white flex items-center gap-1 shadow"
                      style={{ backgroundColor: owner.color }}
                    >
                      <ShieldCheck className="w-3 h-3" /> {owner.name}
                      {ownership?.has_mahal ? " (Hotel)" : ownership?.bhavans ? ` (${ownership.bhavans}H)` : ""}
                    </span>
                  ) : (
                    <span className="text-[10px] font-bold text-emerald-400 bg-emerald-950/80 border border-emerald-800 px-2 py-0.5 rounded">
                      Unowned
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
