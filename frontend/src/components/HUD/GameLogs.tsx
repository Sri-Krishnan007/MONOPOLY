"use client";

import React, { useEffect, useRef } from "react";
import { GameLog } from "@/lib/types";
import { MessageSquareText, Dices, Landmark, ShieldAlert, Sparkles, AlertCircle } from "lucide-react";

interface GameLogsProps {
  logs: GameLog[];
}

export const GameLogs: React.FC<GameLogsProps> = ({ logs }) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  const getLogIcon = (type: string) => {
    switch (type) {
      case "dice":
        return <Dices className="w-3.5 h-3.5 text-amber-400 mt-0.5 flex-shrink-0" />;
      case "property":
        return <Landmark className="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" />;
      case "jail":
        return <ShieldAlert className="w-3.5 h-3.5 text-rose-400 mt-0.5 flex-shrink-0" />;
      case "card":
        return <Sparkles className="w-3.5 h-3.5 text-sky-400 mt-0.5 flex-shrink-0" />;
      case "alert":
        return <AlertCircle className="w-3.5 h-3.5 text-yellow-400 mt-0.5 flex-shrink-0" />;
      default:
        return <span className="w-1.5 h-1.5 rounded-full bg-slate-500 mt-1.5 flex-shrink-0" />;
    }
  };

  return (
    <div className="flex flex-col h-[260px] sm:h-[320px] p-3.5 bg-slate-900/90 rounded-2xl border border-slate-800 backdrop-blur-md shadow-xl select-none">
      <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
        <MessageSquareText className="w-4 h-4 text-amber-400" />
        <h3 className="font-bold text-xs sm:text-sm text-slate-100 uppercase tracking-wider">
          Game Activity Log
        </h3>
      </div>

      <div
        ref={scrollRef}
        className="flex-grow overflow-y-auto mt-2 space-y-1.5 pr-1 text-xs text-slate-300 font-sans"
      >
        {logs.map((log) => (
          <div
            key={log.id}
            className="flex items-start gap-2 p-1.5 rounded-lg bg-slate-950/40 border border-slate-800/40"
          >
            {getLogIcon(log.log_type)}
            <div className="flex-grow">
              <p className="leading-tight text-slate-200">{log.message}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
