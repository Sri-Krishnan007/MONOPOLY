"use client";

import React from "react";
import { BoardSpace, PropertyOwnership, Player } from "@/lib/types";
import { COLOR_GROUP_STYLES, PLAYER_TOKENS } from "@/lib/boardData";
import { 
  Sparkles, ShieldAlert, Tent, Gavel, Train, Zap, Droplets, 
  Receipt, BadgeDollarSign, Clover, Users, Landmark, Store,
  Palmtree, Sun, Anchor, Gem, Flame, Mountain, Coffee, Briefcase,
  Building, Music, Cpu, Laptop, ShoppingBag, Compass,
  Crown, Diamond, Sparkle, Building2
} from "lucide-react";

interface BoardTileProps {
  space: BoardSpace;
  ownership?: PropertyOwnership;
  owner?: Player;
  playersHere: Player[];
  orientation: "bottom" | "left" | "top" | "right" | "corner";
  onInspect: (spaceId: number) => void;
  isCurrentPlayerPosition?: boolean;
}

const ICON_MAP: Record<string, React.ReactNode> = {
  sparkles: <Sparkles className="w-4 h-4 text-amber-400 animate-pulse" />,
  "shield-alert": <ShieldAlert className="w-5 h-5 text-rose-400" />,
  tent: <Tent className="w-5 h-5 text-emerald-400" />,
  gavel: <Gavel className="w-5 h-5 text-rose-500 animate-bounce" />,
  train: <Train className="w-4 h-4 text-sky-400" />,
  zap: <Zap className="w-4 h-4 text-yellow-400" />,
  droplets: <Droplets className="w-4 h-4 text-cyan-400" />,
  receipt: <Receipt className="w-4 h-4 text-orange-400" />,
  "badge-dollar-sign": <BadgeDollarSign className="w-4 h-4 text-amber-400" />,
  clover: <Clover className="w-4 h-4 text-emerald-400" />,
  users: <Users className="w-4 h-4 text-blue-400" />,
  store: <Store className="w-3.5 h-3.5 text-amber-300" />,
  palmtree: <Palmtree className="w-3.5 h-3.5 text-teal-300" />,
  sun: <Sun className="w-3.5 h-3.5 text-yellow-300" />,
  anchor: <Anchor className="w-3.5 h-3.5 text-sky-300" />,
  gem: <Gem className="w-3.5 h-3.5 text-pink-300" />,
  flame: <Flame className="w-3.5 h-3.5 text-orange-300" />,
  mountain: <Mountain className="w-3.5 h-3.5 text-indigo-300" />,
  coffee: <Coffee className="w-3.5 h-3.5 text-amber-400" />,
  briefcase: <Briefcase className="w-3.5 h-3.5 text-amber-300" />,
  building: <Building className="w-3.5 h-3.5 text-sky-300" />,
  music: <Music className="w-3.5 h-3.5 text-rose-300" />,
  cpu: <Cpu className="w-3.5 h-3.5 text-cyan-300" />,
  laptop: <Laptop className="w-3.5 h-3.5 text-blue-300" />,
  "shopping-bag": <ShoppingBag className="w-3.5 h-3.5 text-yellow-300" />,
  "building-2": <Building2 className="w-3.5 h-3.5 text-amber-300" />,
  compass: <Compass className="w-3.5 h-3.5 text-emerald-300" />,
  landmark: <Landmark className="w-3.5 h-3.5 text-emerald-400" />,
  monument: <Landmark className="w-3.5 h-3.5 text-amber-400" />,
  crown: <Crown className="w-3.5 h-3.5 text-yellow-400" />,
  diamond: <Diamond className="w-3.5 h-3.5 text-indigo-300" />,
  sparkle: <Sparkle className="w-3.5 h-3.5 text-indigo-200" />
};

export const BoardTile: React.FC<BoardTileProps> = ({
  space,
  ownership,
  owner,
  playersHere,
  orientation,
  onInspect,
  isCurrentPlayerPosition
}) => {
  const isCorner = orientation === "corner";
  const colorStyle = space.color_group ? COLOR_GROUP_STYLES[space.color_group] : null;

  const getTokenEmoji = (tokenId: string) => {
    const found = PLAYER_TOKENS.find(t => t.id === tokenId);
    return found ? found.icon : "♟️";
  };

  return (
    <div
      onClick={() => onInspect(space.id)}
      className={`relative flex flex-col justify-between p-1 select-none cursor-pointer transition-all duration-200 border border-slate-700/70 bg-slate-900 hover:bg-slate-800 hover:border-amber-400 hover:z-20 hover:shadow-2xl hover:shadow-amber-500/20 ${
        isCurrentPlayerPosition ? "ring-2 ring-amber-400 ring-offset-1 ring-offset-slate-950 z-10 scale-[1.02]" : ""
      } ${
        isCorner ? "w-full h-full bg-slate-950" : ""
      }`}
    >
      {/* Property Color Header */}
      {colorStyle && (
        <div
          className={`h-3 sm:h-3.5 w-full rounded-t-sm mb-0.5 flex items-center justify-between px-1 text-[8px] font-bold ${colorStyle.bg} ${colorStyle.text} shadow`}
        >
          {/* House / Hotel counters */}
          <div className="flex items-center gap-0.5">
            {ownership?.has_mahal ? (
              <span className="bg-red-600 text-white px-1 rounded text-[7px] font-black uppercase tracking-wider animate-pulse">
                HOTEL
              </span>
            ) : ownership?.bhavans ? (
              <div className="flex gap-0.5">
                {Array.from({ length: ownership.bhavans }).map((_, i) => (
                  <span key={i} className="w-1.5 h-1.5 bg-emerald-400 rounded-sm inline-block shadow" />
                ))}
              </div>
            ) : null}
          </div>
          {ownership?.is_mortgaged && (
            <span className="bg-red-950 text-red-300 border border-red-700 px-0.5 rounded text-[6px] font-bold">
              MORTGAGED
            </span>
          )}
        </div>
      )}

      {/* Owner Ribbon Badge (Shows exactly who bought this space) */}
      {owner && (
        <div
          className="w-full py-0.5 px-1 mb-0.5 rounded text-[7px] sm:text-[8px] font-bold text-white flex items-center justify-between shadow"
          style={{ backgroundColor: owner.color }}
          title={`Owned by ${owner.name}`}
        >
          <span className="truncate max-w-[50px] sm:max-w-[65px]">{owner.name}</span>
          <span>{getTokenEmoji(owner.token)}</span>
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex flex-col items-center justify-center flex-grow text-center px-0.5">
        <div className="my-0.5 flex justify-center items-center">
          {ICON_MAP[space.icon] || <Store className="w-3.5 h-3.5 text-slate-400" />}
        </div>

        {/* English Name */}
        <p className="font-black text-[9px] sm:text-[10px] leading-tight text-slate-100 line-clamp-2">
          {space.name}
        </p>

        {/* Monument & City */}
        {space.monument && (
          <p className="text-[7px] sm:text-[8px] text-amber-400 font-semibold leading-tight line-clamp-1">
            {space.monument}
          </p>
        )}

        {/* Price Tag */}
        {space.price > 0 ? (
          <span className="mt-0.5 text-[8px] sm:text-[9px] font-black text-emerald-400">
            ₹{space.price.toLocaleString("en-IN")}
          </span>
        ) : space.type === "go" ? (
          <span className="text-[7px] font-black text-amber-300">COLLECT ₹2,000</span>
        ) : null}
      </div>

      {/* Player Tokens currently on Space */}
      <div className="flex flex-wrap items-center justify-center gap-1 min-h-[16px] mt-0.5 bg-slate-950/80 rounded px-1 border border-slate-800">
        {playersHere.map((p) => (
          <div
            key={p.id}
            title={`${p.name} (₹${p.cash.toLocaleString("en-IN")})`}
            className="flex items-center justify-center w-3.5 h-3.5 sm:w-4 sm:h-4 rounded-full text-[10px] shadow border border-white/40 transition-transform hover:scale-125"
            style={{ backgroundColor: p.color }}
          >
            <span>{getTokenEmoji(p.token)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
