import React from "react";
import { OceanScores } from "../types";

const OCEAN_TRAITS = [
  { key: "openness", label: "Openness", color: "#8b5cf6", description: "Curiosity & creativity" },
  { key: "conscientiousness", label: "Conscientiousness", color: "#3b82f6", description: "Organization & discipline" },
  { key: "extraversion", label: "Extraversion", color: "#f59e0b", description: "Sociability & energy" },
  { key: "agreeableness", label: "Agreeableness", color: "#10b981", description: "Cooperation & trust" },
  { key: "neuroticism", label: "Neuroticism", color: "#ef4444", description: "Emotional sensitivity" },
] as const;

interface OceanScoresProps {
  scores: OceanScores;
  title?: string;
}

export const OceanScoresDisplay: React.FC<OceanScoresProps> = ({ scores, title }) => {
  return (
    <div className="flex flex-col gap-3">
      {title && <h3 className="font-semibold text-gray-700 text-sm">{title}</h3>}
      {OCEAN_TRAITS.map(({ key, label, color, description }) => {
        const value = scores[key as keyof OceanScores] as number;
        const pct = Math.round(value * 100);
        return (
          <div key={key} className="flex flex-col gap-1">
            <div className="flex justify-between items-center">
              <div>
                <span className="text-sm font-medium text-gray-700">{label}</span>
                <span className="text-xs text-gray-400 ml-2">{description}</span>
              </div>
              <span className="text-sm font-bold" style={{ color }}>{pct}%</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div
                className="h-2 rounded-full transition-all duration-500"
                style={{ width: `${pct}%`, backgroundColor: color }}
              />
            </div>
          </div>
        );
      })}
      {scores.confidence !== undefined && (
        <div className="text-xs text-gray-500 text-right mt-1">
          Confidence: {Math.round((scores.confidence || 0) * 100)}%
        </div>
      )}
    </div>
  );
};
