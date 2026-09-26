"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { PLAYER_TOKENS } from "@/lib/boardData";
import { sounds } from "@/lib/sounds";
import { Crown, Play, Users, Bot, Sparkles, Building2, Shield, Flame, BookOpen } from "lucide-react";

export default function LandingPage() {
  const router = useRouter();

  const [playerName, setPlayerName] = useState("Raja Tycoon");
  const [selectedToken, setSelectedToken] = useState(PLAYER_TOKENS[0].id);
  const [roomCode, setRoomCode] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const getApiUrl = () => {
    if (process.env.NEXT_PUBLIC_API_URL) return process.env.NEXT_PUBLIC_API_URL.replace(/\/$/, "");
    if (typeof window !== "undefined") {
      return `http://${window.location.hostname}:8000`;
    }
    return "http://127.0.0.1:8000";
  };

  const handleCreateRoom = async (isSolo: boolean = false) => {
    if (!playerName.trim()) {
      setErrorMsg("Please enter your Tycoon name.");
      return;
    }
    setIsLoading(true);
    setErrorMsg("");

    try {
      const res = await fetch(`${getApiUrl()}/api/rooms/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          host_name: playerName.trim(),
          token: selectedToken
        })
      });

      if (!res.ok) throw new Error("Could not create room");
      const data = await res.json();

      sounds.playCashChime();

      // If solo mode, immediately add 3 AI bots and start!
      if (isSolo) {
        // We will navigate directly and lobby will let user add bots or start
        router.push(`/game/${data.room_id}?playerId=${data.host_id}&solo=true`);
      } else {
        router.push(`/game/${data.room_id}?playerId=${data.host_id}`);
      }
    } catch (err: unknown) {
      setErrorMsg("Could not connect to FastAPI backend server (http://127.0.0.1:8000). Make sure backend is running.");
      setIsLoading(false);
    }
  };

  const handleJoinRoom = async () => {
    if (!playerName.trim()) {
      setErrorMsg("Please enter your Tycoon name.");
      return;
    }
    if (!roomCode.trim()) {
      setErrorMsg("Please enter a valid room code.");
      return;
    }
    setIsLoading(true);
    setErrorMsg("");

    try {
      const res = await fetch(`${getApiUrl()}/api/rooms/join`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          room_code: roomCode.trim().toUpperCase(),
          player_name: playerName.trim(),
          token: selectedToken
        })
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Could not join room");
      }
      const data = await res.json();
      sounds.playBuyProperty();
      router.push(`/game/${data.room_id}?playerId=${data.player_id}`);
    } catch (err: unknown) {
      setErrorMsg(err instanceof Error ? err.message : "Failed to join room");
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-amber-950 text-slate-100 flex flex-col justify-between p-4 sm:p-8 select-none">
      {/* Top Header */}
      <header className="max-w-4xl mx-auto text-center pt-4">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-amber-500/10 border border-amber-400/30 text-amber-300 text-xs font-bold tracking-widest uppercase mb-3">
          <Sparkles className="w-3.5 h-3.5" /> Next.js & FastAPI Indian Monopoly Edition
        </div>
        <h1 className="text-4xl sm:text-6xl font-black tracking-widest uppercase bg-gradient-to-r from-amber-200 via-yellow-400 to-amber-500 bg-clip-text text-transparent drop-shadow-md">
          KUBER
        </h1>
        <p className="text-base sm:text-xl font-bold text-amber-400/90 mt-1">
          THE GREAT INDIAN PROPERTY EMPIRE • भारत का कुबेर
        </p>
        <p className="text-xs sm:text-sm text-slate-400 max-w-xl mx-auto mt-2">
          Conquer iconic Indian commercial hubs from Chandni Chowk to Marine Drive, build Bhavans & Mahals, and build an immortal financial empire.
        </p>
      </header>

      {/* Main Game Setup Card */}
      <main className="max-w-2xl mx-auto w-full my-8 p-6 sm:p-8 bg-slate-900/90 border-2 border-amber-500/80 rounded-3xl shadow-2xl backdrop-blur-md">
        {errorMsg && (
          <div className="mb-6 p-3 bg-red-950/80 border border-red-500 text-red-200 text-xs rounded-xl font-medium text-center animate-pulse">
            {errorMsg}
          </div>
        )}

        {/* Player Name Input */}
        <div className="mb-6">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
            Your Tycoon Name (आपका नाम):
          </label>
          <input
            type="text"
            value={playerName}
            onChange={(e) => setPlayerName(e.target.value)}
            placeholder="e.g. Mukesh Tycoon"
            className="w-full px-4 py-3 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 font-bold text-sm focus:outline-none focus:border-amber-400 transition-colors shadow-inner"
          />
        </div>

        {/* Bespoke Token Selector */}
        <div className="mb-6">
          <label className="block text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">
            Choose Your Metallic Token (शाही मोहरा चुनें):
          </label>
          <div className="grid grid-cols-4 gap-2 sm:gap-3">
            {PLAYER_TOKENS.map((token) => {
              const isSelected = selectedToken === token.id;
              return (
                <button
                  key={token.id}
                  onClick={() => setSelectedToken(token.id)}
                  className={`p-3 rounded-2xl border flex flex-col items-center justify-center transition-all ${
                    isSelected
                      ? "bg-amber-500/20 border-amber-400 ring-2 ring-amber-400/50 scale-105 shadow-lg shadow-amber-500/10"
                      : "bg-slate-950/60 border-slate-800 hover:border-slate-700 opacity-70 hover:opacity-100"
                  }`}
                >
                  <span className="text-2xl sm:text-3xl mb-1">{token.icon}</span>
                  <span className="text-[10px] sm:text-xs font-bold text-slate-200 leading-tight text-center">
                    {token.name}
                  </span>
                  <span className="text-[8px] text-amber-400/80 mt-0.5">{token.finish}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col gap-3">
          {/* Solo Play */}
          <button
            onClick={() => handleCreateRoom(true)}
            disabled={isLoading}
            className="w-full py-3.5 px-6 bg-gradient-to-r from-amber-500 via-yellow-500 to-amber-600 hover:from-amber-400 hover:to-yellow-400 text-slate-950 font-black text-sm rounded-xl shadow-xl shadow-amber-500/20 transform active:scale-95 transition-all flex items-center justify-center gap-2"
          >
            <Bot className="w-5 h-5" /> PLAY VS INDIAN AI TYCOONS (एकल खेल)
          </button>

          {/* Multiplayer Host */}
          <button
            onClick={() => handleCreateRoom(false)}
            disabled={isLoading}
            className="w-full py-3 px-6 bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold text-xs rounded-xl border border-amber-500/40 transition-all flex items-center justify-center gap-2"
          >
            <Crown className="w-4 h-4" /> Host Multiplayer Empire Room (नया कमरा बनाएं)
          </button>

          {/* Join Existing Room */}
          <div className="flex gap-2 mt-2 pt-4 border-t border-slate-800">
            <input
              type="text"
              value={roomCode}
              onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
              placeholder="ENTER ROOM CODE (e.g. KUBER-ABCD)"
              className="flex-grow px-4 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-slate-100 font-mono font-bold text-xs focus:outline-none focus:border-amber-400 uppercase tracking-widest"
            />
            <button
              onClick={handleJoinRoom}
              disabled={isLoading || !roomCode.trim()}
              className="py-2.5 px-5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 text-white font-bold text-xs rounded-xl transition-all shadow"
            >
              Join Room
            </button>
          </div>
        </div>
      </main>

      {/* Feature Highlights Footer */}
      <footer className="max-w-4xl mx-auto w-full grid grid-cols-2 sm:grid-cols-4 gap-3 text-center text-xs pb-4">
        <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
          <Building2 className="w-5 h-5 mx-auto text-amber-400 mb-1" />
          <span className="font-bold text-slate-200 block">22 Indian Cities</span>
          <span className="text-[10px] text-slate-500">8 Property Color Groups</span>
        </div>
        <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
          <Crown className="w-5 h-5 mx-auto text-yellow-400 mb-1" />
          <span className="font-bold text-slate-200 block">₹15,000 Economy</span>
          <span className="text-[10px] text-slate-500">Calibrated Mathematical Balance</span>
        </div>
        <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
          <Shield className="w-5 h-5 mx-auto text-sky-400 mb-1" />
          <span className="font-bold text-slate-200 block">Bhavans & Mahals</span>
          <span className="text-[10px] text-slate-500">Authentic Indian Architecture</span>
        </div>
        <div className="p-3 bg-slate-900/60 rounded-xl border border-slate-800">
          <Flame className="w-5 h-5 mx-auto text-rose-400 mb-1" />
          <span className="font-bold text-slate-200 block">Kismat & Panchayat</span>
          <span className="text-[10px] text-slate-500">32 Bespoke Event Decks</span>
        </div>
      </footer>
    </div>
  );
}
