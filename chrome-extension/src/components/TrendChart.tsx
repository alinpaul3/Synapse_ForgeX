import React from "react";
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { OceanScores } from "../types";

interface RadarChartProps {
  scores: OceanScores;
  youtubeScores?: OceanScores | null;
  redditScores?: OceanScores | null;
}

const TRAITS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"];
const TRAIT_LABELS: Record<string, string> = {
  openness: "Open",
  conscientiousness: "Consc.",
  extraversion: "Extra.",
  agreeableness: "Agree.",
  neuroticism: "Neuro.",
};

export const OceanRadarChart: React.FC<RadarChartProps> = ({ scores, youtubeScores, redditScores }) => {
  const data = TRAITS.map((trait) => ({
    trait: TRAIT_LABELS[trait],
    Final: Math.round((scores[trait as keyof OceanScores] as number) * 100),
    ...(youtubeScores && { YouTube: Math.round((youtubeScores[trait as keyof OceanScores] as number) * 100) }),
    ...(redditScores && { Reddit: Math.round((redditScores[trait as keyof OceanScores] as number) * 100) }),
  }));

  return (
    <ResponsiveContainer width="100%" height={220}>
      <RadarChart data={data}>
        <PolarGrid stroke="#e5e7eb" />
        <PolarAngleAxis dataKey="trait" tick={{ fontSize: 11, fill: "#6b7280" }} />
        <Radar name="Final" dataKey="Final" stroke="#4f6ef7" fill="#4f6ef7" fillOpacity={0.3} />
        {youtubeScores && (
          <Radar name="YouTube" dataKey="YouTube" stroke="#ef4444" fill="#ef4444" fillOpacity={0.15} />
        )}
        {redditScores && (
          <Radar name="Reddit" dataKey="Reddit" stroke="#f97316" fill="#f97316" fillOpacity={0.15} />
        )}
        <Legend wrapperStyle={{ fontSize: "11px" }} />
      </RadarChart>
    </ResponsiveContainer>
  );
};

interface TrendPoint {
  date: string;
  openness?: number;
  conscientiousness?: number;
  extraversion?: number;
  agreeableness?: number;
  neuroticism?: number;
}

interface TrendChartProps {
  data: TrendPoint[];
}

export const TrendChart: React.FC<TrendChartProps> = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="flex items-center justify-center h-32 text-gray-400 text-sm">
        No trend data available yet
      </div>
    );
  }

  return (
    <ResponsiveContainer width="100%" height={180}>
      <LineChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="date" tick={{ fontSize: 10, fill: "#9ca3af" }} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 10, fill: "#9ca3af" }} />
        <Tooltip formatter={(v: number) => `${v}%`} />
        <Line type="monotone" dataKey="openness" stroke="#8b5cf6" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="conscientiousness" stroke="#3b82f6" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="extraversion" stroke="#f59e0b" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="agreeableness" stroke="#10b981" dot={false} strokeWidth={2} />
        <Line type="monotone" dataKey="neuroticism" stroke="#ef4444" dot={false} strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
};
