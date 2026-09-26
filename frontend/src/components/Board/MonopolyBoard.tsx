"use client";

import React from "react";
import { GameState } from "@/lib/types";
import { BOARD_SPACES } from "@/lib/boardData";
import { BoardTile } from "./BoardTile";
import { CenterConsole } from "./CenterConsole";

interface MonopolyBoardProps {
  game: GameState;
  myPlayerId: string;
  onInspectSpace: (spaceId: number) => void;
  onRollDice: () => void;
  onBuyProperty: (spaceId: number) => void;
  onDeclineBuy: (spaceId: number) => void;
  onPayBail: () => void;
  onUseJailCard: () => void;
  onEndTurn: () => void;
  onOpenPortfolio: () => void;
}

export const MonopolyBoard: React.FC<MonopolyBoardProps> = ({
  game,
  myPlayerId,
  onInspectSpace,
  onRollDice,
  onBuyProperty,
  onDeclineBuy,
  onPayBail,
  onUseJailCard,
  onEndTurn,
  onOpenPortfolio,
}) => {
  const curPlayer = game.players[game.current_player_index];
  const curSpace = curPlayer ? BOARD_SPACES[curPlayer.position] : undefined;

  const getPlayersOnSpace = (spaceId: number) => {
    return game.players.filter((p) => p.position === spaceId && !p.is_bankrupt);
  };

  const getSpace = (id: number) => {
    return BOARD_SPACES[id] || BOARD_SPACES[0];
  };

  return (
    <div className="w-full max-w-[950px] aspect-square mx-auto p-2 sm:p-4 bg-slate-950 rounded-3xl shadow-2xl border-2 border-amber-600/40 select-none">
      {/* 11x11 CSS Grid Board Layout */}
      <div className="w-full h-full grid grid-cols-11 grid-rows-11 gap-1 relative rounded-2xl overflow-hidden bg-slate-900/50 p-1 border border-slate-800">
        {/* --- TOP ROW: Positions 20 to 30 --- */}
        {/* Pos 20: Vishram Sthal (Corner: Row 0, Col 0) */}
        <div className="col-start-1 row-start-1">
          <BoardTile
            space={getSpace(20)}
            ownership={game.properties[20]}
            playersHere={getPlayersOnSpace(20)}
            orientation="corner"
            onInspect={onInspectSpace}
            isCurrentPlayerPosition={curPlayer?.position === 20}
          />
        </div>
        {/* Pos 21 to 29 (Row 0, Cols 1 to 9) */}
        {[21, 22, 23, 24, 25, 26, 27, 28, 29].map((pos, idx) => (
          <div key={pos} style={{ gridColumnStart: idx + 2, gridRowStart: 1 }}>
            <BoardTile
              space={getSpace(pos)}
              ownership={game.properties[pos]}
              playersHere={getPlayersOnSpace(pos)}
              orientation="top"
              onInspect={onInspectSpace}
              isCurrentPlayerPosition={curPlayer?.position === pos}
            />
          </div>
        ))}
        {/* Pos 30: Nyayalay Saman / Go to Jail (Corner: Row 0, Col 10) */}
        <div className="col-start-11 row-start-1">
          <BoardTile
            space={getSpace(30)}
            ownership={game.properties[30]}
            playersHere={getPlayersOnSpace(30)}
            orientation="corner"
            onInspect={onInspectSpace}
            isCurrentPlayerPosition={curPlayer?.position === 30}
          />
        </div>

        {/* --- RIGHT COLUMN: Positions 31 to 39 (Col 10, Rows 1 to 9) --- */}
        {[31, 32, 33, 34, 35, 36, 37, 38, 39].map((pos, idx) => (
          <div key={pos} style={{ gridColumnStart: 11, gridRowStart: idx + 2 }}>
            <BoardTile
              space={getSpace(pos)}
              ownership={game.properties[pos]}
              playersHere={getPlayersOnSpace(pos)}
              orientation="right"
              onInspect={onInspectSpace}
              isCurrentPlayerPosition={curPlayer?.position === pos}
            />
          </div>
        ))}

        {/* --- BOTTOM ROW: Positions 10 to 0 (Row 10, Cols 0 to 10) --- */}
        {/* Pos 10: Police Chowki / Jail (Corner: Row 10, Col 0) */}
        <div className="col-start-1 row-start-11">
          <BoardTile
            space={getSpace(10)}
            ownership={game.properties[10]}
            playersHere={getPlayersOnSpace(10)}
            orientation="corner"
            onInspect={onInspectSpace}
            isCurrentPlayerPosition={curPlayer?.position === 10}
          />
        </div>
        {/* Pos 9 down to 1 (Row 10, Cols 1 to 9) */}
        {[9, 8, 7, 6, 5, 4, 3, 2, 1].map((pos, idx) => (
          <div key={pos} style={{ gridColumnStart: idx + 2, gridRowStart: 11 }}>
            <BoardTile
              space={getSpace(pos)}
              ownership={game.properties[pos]}
              playersHere={getPlayersOnSpace(pos)}
              orientation="bottom"
              onInspect={onInspectSpace}
              isCurrentPlayerPosition={curPlayer?.position === pos}
            />
          </div>
        ))}
        {/* Pos 0: Aarambh / GO (Corner: Row 10, Col 10) */}
        <div className="col-start-11 row-start-11">
          <BoardTile
            space={getSpace(0)}
            ownership={game.properties[0]}
            playersHere={getPlayersOnSpace(0)}
            orientation="corner"
            onInspect={onInspectSpace}
            isCurrentPlayerPosition={curPlayer?.position === 0}
          />
        </div>

        {/* --- LEFT COLUMN: Positions 11 to 19 (Col 0, Rows 9 down to 1) --- */}
        {[19, 18, 17, 16, 15, 14, 13, 12, 11].map((pos, idx) => (
          <div key={pos} style={{ gridColumnStart: 1, gridRowStart: idx + 2 }}>
            <BoardTile
              space={getSpace(pos)}
              ownership={game.properties[pos]}
              playersHere={getPlayersOnSpace(pos)}
              orientation="left"
              onInspect={onInspectSpace}
              isCurrentPlayerPosition={curPlayer?.position === pos}
            />
          </div>
        ))}

        {/* --- CENTER BOARD AREA: Rows 2 to 10, Cols 2 to 10 (9x9 Area) --- */}
        <div className="col-start-2 col-end-11 row-start-2 row-end-11 p-2 sm:p-4 flex items-center justify-center">
          <CenterConsole
            game={game}
            myPlayerId={myPlayerId}
            currentSpace={curSpace}
            onRollDice={onRollDice}
            onBuyProperty={onBuyProperty}
            onDeclineBuy={onDeclineBuy}
            onPayBail={onPayBail}
            onUseJailCard={onUseJailCard}
            onEndTurn={onEndTurn}
            onOpenPortfolio={onOpenPortfolio}
          />
        </div>
      </div>
    </div>
  );
};
