import React, { useState } from "react";
import { Platform, ConsentData } from "../types";
import { useAppStore } from "../store/appStore";

interface ConsentScreenProps {
  platforms: Platform[];
  onAgree: (consent: ConsentData) => void;
  onBack: () => void;
}

export const ConsentScreen: React.FC<ConsentScreenProps> = ({ platforms, onAgree, onBack }) => {
  const [historicalAllowed, setHistoricalAllowed] = useState(true);
  const [syncAllowed, setSyncAllowed] = useState(true);
  const [agreed, setAgreed] = useState(false);
  const { isLoading } = useAppStore();

  const handleAgree = () => {
    if (!agreed) return;
    onAgree({
      platforms,
      historical_allowed: historicalAllowed,
      sync_allowed: syncAllowed,
    });
  };

  return (
    <div className="flex flex-col gap-4 p-4">
      <div className="text-center">
        <div className="text-3xl mb-2">🔒</div>
        <h2 className="text-xl font-bold text-gray-800">Data Consent</h2>
        <p className="text-sm text-gray-500 mt-1">
          Review how your data will be used
        </p>
      </div>

      <div className="bg-gray-50 rounded-lg p-3 text-xs text-gray-600 space-y-2 max-h-40 overflow-y-auto">
        <p className="font-semibold text-gray-700">What we collect:</p>
        {platforms.includes("youtube") && (
          <p>• YouTube: channel info, video descriptions, your public comments</p>
        )}
        {platforms.includes("reddit") && (
          <p>• Reddit: your posts, comments, and subreddit activity</p>
        )}
        <p className="font-semibold text-gray-700 mt-2">How we use it:</p>
        <p>• Generate your OCEAN personality profile using ML models</p>
        <p>• Display insights in your personal dashboard</p>
        <p className="font-semibold text-gray-700 mt-2">Your rights:</p>
        <p>• Revoke consent at any time</p>
        <p>• Request complete data deletion</p>
        <p>• Disconnect individual platforms</p>
      </div>

      <div className="flex flex-col gap-3">
        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={historicalAllowed}
            onChange={(e) => setHistoricalAllowed(e.target.checked)}
            className="mt-0.5 w-4 h-4 accent-blue-600"
          />
          <div>
            <div className="text-sm font-medium text-gray-700">Historical data fetch</div>
            <div className="text-xs text-gray-500">Fetch past posts/comments for initial analysis</div>
          </div>
        </label>

        <label className="flex items-start gap-3 cursor-pointer">
          <input
            type="checkbox"
            checked={syncAllowed}
            onChange={(e) => setSyncAllowed(e.target.checked)}
            className="mt-0.5 w-4 h-4 accent-blue-600"
          />
          <div>
            <div className="text-sm font-medium text-gray-700">Future sync</div>
            <div className="text-xs text-gray-500">Periodically fetch new data to keep your profile updated</div>
          </div>
        </label>

        <label className="flex items-start gap-3 cursor-pointer border-t pt-3">
          <input
            type="checkbox"
            checked={agreed}
            onChange={(e) => setAgreed(e.target.checked)}
            className="mt-0.5 w-4 h-4 accent-blue-600"
          />
          <div className="text-sm font-medium text-gray-700">
            I agree to the data usage terms above
          </div>
        </label>
      </div>

      <div className="flex gap-2">
        <button
          onClick={onBack}
          className="flex-1 py-2 px-4 rounded-lg border border-gray-300 text-gray-600 font-semibold hover:bg-gray-50 transition-all"
        >
          Back
        </button>
        <button
          onClick={handleAgree}
          disabled={!agreed || isLoading}
          className={`flex-1 py-2 px-4 rounded-lg font-semibold transition-all ${
            agreed && !isLoading
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : "bg-gray-200 text-gray-400 cursor-not-allowed"
          }`}
        >
          {isLoading ? "Connecting..." : "Agree & Connect"}
        </button>
      </div>
    </div>
  );
};
