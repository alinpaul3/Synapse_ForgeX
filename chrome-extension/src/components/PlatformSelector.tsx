import React, { useState } from "react";
import { Platform } from "../types";
import { useAppStore } from "../store/appStore";

interface PlatformSelectorProps {
  onNext: (platforms: Platform[]) => void;
}

const PLATFORM_INFO = {
  youtube: {
    name: "YouTube",
    description: "Analyze your video comments, descriptions, and interactions",
    icon: "▶",
    color: "bg-red-500",
  },
  reddit: {
    name: "Reddit",
    description: "Analyze your posts, comments, and community interactions",
    icon: "🔴",
    color: "bg-orange-500",
  },
} as const;

export const PlatformSelector: React.FC<PlatformSelectorProps> = ({ onNext }) => {
  const [selected, setSelected] = useState<Set<Platform>>(new Set());
  const { error } = useAppStore();

  const toggle = (platform: Platform) => {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(platform)) {
        next.delete(platform);
      } else {
        next.add(platform);
      }
      return next;
    });
  };

  const handleNext = () => {
    if (selected.size > 0) {
      onNext(Array.from(selected));
    }
  };

  return (
    <div className="flex flex-col gap-4 p-4">
      <div className="text-center">
        <h2 className="text-xl font-bold text-gray-800">Select Platforms</h2>
        <p className="text-sm text-gray-500 mt-1">
          Choose which platforms to analyze for your personality profile
        </p>
      </div>

      <div className="flex flex-col gap-3">
        {(Object.keys(PLATFORM_INFO) as Platform[]).map((platform) => {
          const info = PLATFORM_INFO[platform];
          const isSelected = selected.has(platform);
          return (
            <button
              key={platform}
              onClick={() => toggle(platform)}
              className={`flex items-center gap-3 p-3 rounded-lg border-2 transition-all text-left ${
                isSelected
                  ? "border-blue-500 bg-blue-50"
                  : "border-gray-200 bg-white hover:border-gray-300"
              }`}
            >
              <div className={`w-10 h-10 ${info.color} rounded-lg flex items-center justify-center text-white text-lg flex-shrink-0`}>
                {info.icon}
              </div>
              <div className="flex-1">
                <div className="font-semibold text-gray-800">{info.name}</div>
                <div className="text-xs text-gray-500">{info.description}</div>
              </div>
              <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                isSelected ? "border-blue-500 bg-blue-500" : "border-gray-300"
              }`}>
                {isSelected && <span className="text-white text-xs">✓</span>}
              </div>
            </button>
          );
        })}
      </div>

      {error && (
        <div className="text-red-500 text-sm text-center">{error}</div>
      )}

      <button
        onClick={handleNext}
        disabled={selected.size === 0}
        className={`w-full py-2 px-4 rounded-lg font-semibold transition-all ${
          selected.size > 0
            ? "bg-blue-600 text-white hover:bg-blue-700"
            : "bg-gray-200 text-gray-400 cursor-not-allowed"
        }`}
      >
        Continue ({selected.size} selected)
      </button>
    </div>
  );
};
