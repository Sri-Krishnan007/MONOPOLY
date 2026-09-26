"use client";

import React from "react";
import { BoardSpace, PropertyOwnership, Player } from "@/lib/types";
import { COLOR_GROUP_STYLES } from "@/lib/boardData";
import { X, Building2, Home, Landmark } from "lucide-react";

interface DeedModalProps {
  space?: BoardSpace;
  ownership?: PropertyOwnership;
  owner?: Player;
  onClose: () => void;
}

export const DeedModal: React.FC<DeedModalProps> = ({
  space,
  ownership,
  owner,
  onClose
}) => {
  if (!space) return null;

  const colorStyle = space.color_group ? COLOR_GROUP_STYLES[space.color_group] : null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-md p-6 bg-slate-900 border-2 border-amber-500/80 rounded-3xl shadow-2xl text-slate-100 select-none">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-full bg-slate-800 text-slate-300 hover:text-white hover:bg-slate-700 transition-all"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Deed Title Header */}
        <div className="text-center pb-3 border-b border-slate-800">
          <span className="text-[10px] font-bold tracking-widest text-amber-500 uppercase">
            TITLE DEED CERTIFICATE • स्वामित्व प्रमाण पत्र
          </span>
          {colorStyle && (
            <div
              className={`mt-2 py-2 px-4 rounded-xl font-black text-lg ${colorStyle.bg} ${colorStyle.text} shadow-md uppercase`}
            >
              {space.name}
            </div>
          )}
          {!colorStyle && (
            <h3 className="text-xl font-black text-amber-400 mt-2">{space.name}</h3>
          )}
          <p className="text-xs text-amber-300/80 mt-1 font-semibold">{space.hindi_name}</p>
        </div>

        {/* Ownership Status */}
        <div className="my-3 py-2 px-3 bg-slate-950/80 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
          <span className="text-slate-400">Current Owner:</span>
          {owner ? (
            <span className="font-bold text-amber-400 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full" style={{ backgroundColor: owner.color }} />
              {owner.name}
            </span>
          ) : (
            <span className="font-semibold text-emerald-400">Available from Bank (₹{space.price.toLocaleString("en-IN")})</span>
          )}
        </div>

        {/* Rent Progression Table for Properties */}
        {space.type === "property" && (
          <div className="space-y-1.5 text-xs bg-slate-950 p-3 rounded-2xl border border-slate-800 my-3">
            <div className="flex justify-between py-1 border-b border-slate-800/80">
              <span className="text-slate-300">Base Land Rent</span>
              <span className="font-bold text-emerald-400">₹{space.base_rent.toLocaleString("en-IN")}</span>
            </div>
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>With 1 Bhavan (House)</span>
              <span className="font-semibold text-emerald-400">₹{space.rent_1_house.toLocaleString("en-IN")}</span>
            </div>
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>With 2 Bhavans</span>
              <span className="font-semibold text-emerald-400">₹{space.rent_2_house.toLocaleString("en-IN")}</span>
            </div>
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>With 3 Bhavans</span>
              <span className="font-semibold text-emerald-400">₹{space.rent_3_house.toLocaleString("en-IN")}</span>
            </div>
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>With 4 Bhavans</span>
              <span className="font-semibold text-emerald-400">₹{space.rent_4_house.toLocaleString("en-IN")}</span>
            </div>
            <div className="flex justify-between py-1 border-t border-slate-800 font-bold text-amber-300">
              <span>With Luxury MAHAL (Hotel)</span>
              <span className="text-amber-400">₹{space.rent_hotel.toLocaleString("en-IN")}</span>
            </div>
          </div>
        )}

        {/* Transportation Rent Table */}
        {space.type === "transport" && (
          <div className="space-y-1.5 text-xs bg-slate-950 p-3 rounded-2xl border border-slate-800 my-3">
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>If 1 Transport Hub is owned</span>
              <span className="font-semibold text-emerald-400">₹250</span>
            </div>
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>If 2 Transport Hubs are owned</span>
              <span className="font-semibold text-emerald-400">₹500</span>
            </div>
            <div className="flex justify-between py-0.5 text-slate-300">
              <span>If 3 Transport Hubs are owned</span>
              <span className="font-semibold text-emerald-400">₹1,000</span>
            </div>
            <div className="flex justify-between py-0.5 font-bold text-amber-300">
              <span>If all 4 Transport Hubs are owned</span>
              <span className="text-amber-400">₹2,000</span>
            </div>
          </div>
        )}

        {/* Construction & Mortgage Values */}
        {space.price > 0 && (
          <div className="grid grid-cols-2 gap-2 text-center text-xs my-3">
            {space.house_cost > 0 && (
              <div className="p-2 bg-slate-950 rounded-xl border border-slate-800">
                <span className="text-slate-400 block text-[10px]">Bhavan Cost</span>
                <span className="font-bold text-slate-200">₹{space.house_cost.toLocaleString("en-IN")} each</span>
              </div>
            )}
            <div className="p-2 bg-slate-950 rounded-xl border border-slate-800">
              <span className="text-slate-400 block text-[10px]">Mortgage Value</span>
              <span className="font-bold text-amber-400">₹{space.mortgage_value.toLocaleString("en-IN")}</span>
            </div>
          </div>
        )}

        {/* Description */}
        <p className="text-xs text-slate-400 italic bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/60">
          {space.description}
        </p>
      </div>
    </div>
  );
};
