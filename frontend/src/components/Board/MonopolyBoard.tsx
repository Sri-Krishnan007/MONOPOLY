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
    <div className="w-full max-w-[820px] aspect-square mx-auto p-1.5 sm:p-3 bg-slate-950 rounded-2xl sm:rounded-3xl shadow-2xl border-2 border-amber-600/40 select-none">
      <div className="w-full h-full grid grid-cols-11 grid-rows-11 gap-0.5 sm:gap-1 relative rounded-xl overflow-hidden bg-slate-900/50 p-0.5 border border-slate-800">
        {/* TOP ROW: 20 (Free Parking) -> 30 (Go To Jail) */}
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

        {/* RIGHT COLUMN: 31 -> 39 */}
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

        {/* BOTTOM ROW: 10 (Jail) -> 0 (GO) */}
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

        {/* LEFT COLUMN: 19 down to 11 */}
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

        {/* CENTER BOARD AREA */}
        <div className="col-start-2 col-end-11 row-start-2 row-end-11 p-1 sm:p-2 flex items-center justify-center">
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
