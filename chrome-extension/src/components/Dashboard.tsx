import React, { useEffect, useState } from "react";
import { useAppStore } from "../store/appStore";
import { OceanScoresDisplay } from "./OceanScores";
import { OceanRadarChart, TrendChart } from "./TrendChart";
import { Platform } from "../types";

export const Dashboard: React.FC = () => {
  const {
    userId,
    oceanScores,
    platformScores,
    lastUpdated,
    connectedPlatforms,
    isLoading,
    error,
    fetchProfile,
    triggerSync,
    setView,
  } = useAppStore();

  const [syncing, setSyncing] = useState<Platform | null>(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleSync = async (platform: Platform) => {
    setSyncing(platform);
    try {
      await triggerSync(platform, false);
      setTimeout(() => fetchProfile(), 3000);
    } finally {
      setSyncing(null);
    }
  };

  const formatDate = (iso: string | null) => {
    if (!iso) return "Never";
    try {
      return new Date(iso).toLocaleString();
    } catch {
      return iso;
    }
  };

  return (
    <div className="flex flex-col h-full overflow-auto bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-3 flex items-center justify-between flex-shrink-0">
        <div>
          <h1 className="font-bold text-base">Synapse ForgeX</h1>
          <p className="text-xs text-blue-200">OCEAN Personality Profile</p>
        </div>
        <button
          onClick={() => setView("settings")}
          className="text-blue-200 hover:text-white transition-colors text-lg"
          title="Settings"
        >
          ⚙
        </button>
      </div>

      <div className="flex-1 p-4 space-y-4 overflow-auto">
        {/* Loading state */}
        {isLoading && !oceanScores && (
          <div className="flex flex-col items-center justify-center py-12 gap-3">
            <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <p className="text-gray-500 text-sm">Loading your profile...</p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-600 text-sm">
            {error}
          </div>
        )}

        {/* No scores yet */}
        {!isLoading && !oceanScores && !error && (
          <div className="flex flex-col items-center justify-center py-8 gap-3 text-center">
            <div className="text-4xl">📊</div>
            <h3 className="font-semibold text-gray-700">No profile yet</h3>
            <p className="text-sm text-gray-500">
              Trigger a sync to generate your personality profile
            </p>
            <div className="flex gap-2 mt-2">
              {connectedPlatforms.map((platform) => (
                <button
                  key={platform}
                  onClick={() => handleSync(platform)}
                  disabled={syncing === platform}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-60 transition-all"
                >
                  {syncing === platform ? "Syncing..." : `Sync ${platform}`}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Scores available */}
        {oceanScores && (
          <>
            {/* Last updated */}
            <div className="text-xs text-gray-400 text-right">
              Last updated: {formatDate(lastUpdated)}
            </div>

            {/* Radar chart */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-700 mb-3 text-sm">OCEAN Profile Overview</h3>
              <OceanRadarChart
                scores={oceanScores}
                youtubeScores={platformScores.youtube}
                redditScores={platformScores.reddit}
              />
            </div>

            {/* Final OCEAN scores */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <OceanScoresDisplay scores={oceanScores} title="Final Profile" />
            </div>

            {/* Platform-specific scores */}
            {(platformScores.youtube || platformScores.reddit) && (
              <div className="bg-white rounded-xl shadow-sm p-4 space-y-4">
                <h3 className="font-semibold text-gray-700 text-sm">Platform Breakdown</h3>
                {platformScores.youtube && (
                  <OceanScoresDisplay scores={platformScores.youtube} title="▶ YouTube" />
                )}
                {platformScores.reddit && (
                  <OceanScoresDisplay scores={platformScores.reddit} title="🔴 Reddit" />
                )}
              </div>
            )}

            {/* Trend placeholder */}
            <div className="bg-white rounded-xl shadow-sm p-4">
              <h3 className="font-semibold text-gray-700 mb-3 text-sm">Trend Over Time</h3>
              <TrendChart data={[]} />
            </div>

            {/* Sync buttons */}
            <div className="flex gap-2">
              {connectedPlatforms.map((platform) => (
                <button
                  key={platform}
                  onClick={() => handleSync(platform)}
                  disabled={syncing === platform}
                  className="flex-1 py-2 px-3 bg-blue-50 text-blue-600 rounded-lg text-sm font-medium hover:bg-blue-100 disabled:opacity-60 transition-all border border-blue-200"
                >
                  {syncing === platform ? "Syncing..." : `↻ Sync ${platform}`}
                </button>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};
