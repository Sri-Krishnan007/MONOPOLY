"use client";

import React, { useEffect, useState } from "react";
import { AuctionState, Player } from "@/lib/types";
import { BOARD_SPACES } from "@/lib/boardData";
import { Hammer, Clock, ArrowUpCircle, Check } from "lucide-react";

interface AuctionModalProps {
  auction: AuctionState;
  players: Player[];
  myPlayerId: string;
  onPlaceBid: (amount: number) => void;
  onConcludeAuction: () => void;
}

export const AuctionModal: React.FC<AuctionModalProps> = ({
  auction,
  players,
  myPlayerId,
  onPlaceBid,
  onConcludeAuction
}) => {
  const space = BOARD_SPACES.find(s => s.id === auction.space_id);
  const highestBidder = players.find(p => p.id === auction.highest_bidder_id);
  const me = players.find(p => p.id === myPlayerId);

  const [timeLeft, setTimeLeft] = useState(10);

  useEffect(() => {
    const timer = setInterval(() => {
      const remaining = Math.max(0, Math.ceil(auction.expires_at - Date.now() / 1000));
      setTimeLeft(remaining);
      if (remaining <= 0) {
        clearInterval(timer);
        onConcludeAuction();
      }
    }, 500);

    return () => clearInterval(timer);
  }, [auction.expires_at, onConcludeAuction]);

  if (!space) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/85 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-lg p-6 bg-slate-900 border-2 border-amber-500/80 rounded-3xl shadow-2xl text-center select-none">
        {/* Auction Header */}
        <div className="flex items-center justify-center gap-2 mb-2 text-amber-400">
          <Hammer className="w-6 h-6 animate-bounce" />
          <h2 className="text-xl font-black tracking-wider uppercase">
            PUBLIC REAL ESTATE AUCTION (सार्वजनिक नीलामी)
          </h2>
        </div>

        {/* Property Being Auctioned */}
        <div className="my-4 p-4 bg-slate-950 rounded-2xl border border-slate-800 flex flex-col items-center">
          <span className="text-xs font-bold text-amber-500 uppercase tracking-widest">
            {space.city}, {space.state}
          </span>
          <h3 className="text-2xl font-black text-slate-100">{space.name}</h3>
          <p className="text-sm font-semibold text-amber-400/90">{space.hindi_name}</p>
          <span className="text-xs text-slate-400 mt-1">Bank List Price: ₹{space.price.toLocaleString("en-IN")}</span>
        </div>

        {/* Current Highest Bid & Timer */}
        <div className="grid grid-cols-2 gap-3 my-4">
          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 block mb-1">Current High Bid</span>
            <span className="text-2xl font-black text-emerald-400">
              ₹{auction.current_bid.toLocaleString("en-IN")}
            </span>
            <span className="text-[11px] text-amber-300 block truncate mt-0.5">
              By: {highestBidder?.name || "Starting Call"}
            </span>
          </div>

          <div className="p-3 bg-slate-950 rounded-xl border border-slate-800 flex flex-col items-center justify-center">
            <span className="text-xs text-slate-400 flex items-center gap-1 mb-1">
              <Clock className="w-3.5 h-3.5 text-rose-400" /> Auction Timer
            </span>
            <span className={`text-2xl font-black ${timeLeft <= 3 ? "text-rose-500 animate-ping" : "text-amber-400"}`}>
              {timeLeft}s
            </span>
            <span className="text-[10px] text-slate-500">Hammer falls at 0s</span>
          </div>
        </div>

        {/* Quick Bidding Controls */}
        <div className="flex flex-col gap-2 mt-4">
          <span className="text-xs font-semibold text-slate-300">Raise the Bid (बोली लगाएं):</span>
          <div className="grid grid-cols-3 gap-2">
            {[100, 500, 1000].map((increment) => {
              const nextBid = auction.current_bid + increment;
              const canAfford = (me?.cash || 0) >= nextBid;
              return (
                <button
                  key={increment}
                  onClick={() => onPlaceBid(nextBid)}
                  disabled={!canAfford}
                  className="py-2.5 px-2 bg-gradient-to-r from-amber-600 to-yellow-600 hover:from-amber-500 hover:to-yellow-500 disabled:opacity-40 text-slate-950 font-black rounded-xl text-xs transition-all shadow-md flex items-center justify-center gap-1"
                >
                  <ArrowUpCircle className="w-3.5 h-3.5" /> +₹{increment} (₹{nextBid.toLocaleString("en-IN")})
                </button>
              );
            })}
          </div>
          <p className="text-[11px] text-slate-400 mt-1">
            Your Cash Balance: <strong className="text-emerald-400">₹{(me?.cash || 0).toLocaleString("en-IN")}</strong>
          </p>
        </div>
      </div>
    </div>
  );
};
