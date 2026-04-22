import React, { useState } from "react";
import { useAppStore } from "../store/appStore";
import { Platform } from "../types";

export const Settings: React.FC = () => {
  const {
    userId,
    connectedPlatforms,
    isLoading,
    error,
    disconnectPlatform,
    deleteAccount,
    revokeConsent,
    logout,
    setView,
  } = useAppStore();

  const [confirmDelete, setConfirmDelete] = useState(false);
  const [confirmRevoke, setConfirmRevoke] = useState(false);

  const handleDisconnect = async (platform: Platform) => {
    if (window.confirm(`Disconnect ${platform}? Your ${platform} data will remain stored.`)) {
      await disconnectPlatform(platform);
    }
  };

  const handleDelete = async () => {
    if (!confirmDelete) {
      setConfirmDelete(true);
      return;
    }
    await deleteAccount();
  };

  const handleRevoke = async () => {
    if (!confirmRevoke) {
      setConfirmRevoke(true);
      return;
    }
    await revokeConsent();
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-4 py-3 flex items-center gap-3 flex-shrink-0">
        <button
          onClick={() => setView("dashboard")}
          className="text-gray-500 hover:text-gray-700 text-lg"
        >
          ←
        </button>
        <h2 className="font-bold text-gray-800">Settings</h2>
      </div>

      <div className="flex-1 overflow-auto p-4 space-y-4">
        {/* Account info */}
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="font-semibold text-gray-700 text-sm mb-2">Account</h3>
          <div className="text-xs text-gray-400 break-all">
            User ID: {userId || "Not connected"}
          </div>
        </div>

        {/* Connected platforms */}
        <div className="bg-white rounded-xl shadow-sm p-4">
          <h3 className="font-semibold text-gray-700 text-sm mb-3">Connected Platforms</h3>
          {connectedPlatforms.length === 0 ? (
            <p className="text-xs text-gray-400">No platforms connected</p>
          ) : (
            <div className="space-y-2">
              {connectedPlatforms.map((platform) => (
                <div key={platform} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full" />
                    <span className="text-sm text-gray-700 capitalize">{platform}</span>
                  </div>
                  <button
                    onClick={() => handleDisconnect(platform)}
                    disabled={isLoading}
                    className="text-xs text-red-500 hover:text-red-700 font-medium transition-colors"
                  >
                    Disconnect
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Danger zone */}
        <div className="bg-white rounded-xl shadow-sm p-4 border border-red-100">
          <h3 className="font-semibold text-red-600 text-sm mb-3">⚠ Danger Zone</h3>

          <div className="space-y-3">
            <div>
              <button
                onClick={handleRevoke}
                disabled={isLoading}
                className={`w-full py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                  confirmRevoke
                    ? "bg-orange-500 text-white hover:bg-orange-600"
                    : "bg-orange-50 text-orange-600 border border-orange-200 hover:bg-orange-100"
                }`}
              >
                {confirmRevoke ? "⚠ Click again to confirm revoke" : "Revoke Consent"}
              </button>
              <p className="text-xs text-gray-400 mt-1">
                Stops all future data collection and processing
              </p>
            </div>

            <div>
              <button
                onClick={handleDelete}
                disabled={isLoading}
                className={`w-full py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                  confirmDelete
                    ? "bg-red-600 text-white hover:bg-red-700"
                    : "bg-red-50 text-red-600 border border-red-200 hover:bg-red-100"
                }`}
              >
                {confirmDelete ? "⚠ Click again to delete all data" : "Delete All My Data"}
              </button>
              <p className="text-xs text-gray-400 mt-1">
                Permanently deletes all stored data and your account
              </p>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-3 text-red-600 text-xs">
            {error}
          </div>
        )}

        {/* Sign out */}
        <button
          onClick={logout}
          className="w-full py-2 px-4 rounded-lg border border-gray-300 text-gray-600 text-sm font-medium hover:bg-gray-50 transition-all"
        >
          Sign Out
        </button>
      </div>
    </div>
  );
};
