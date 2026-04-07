import React, { useEffect } from "react";
import { useAppStore } from "../store/appStore";
import { PlatformSelector } from "../components/PlatformSelector";
import { ConsentScreen } from "../components/ConsentScreen";
import { Dashboard } from "../components/Dashboard";
import { Settings } from "../components/Settings";
import { Platform, ConsentData } from "../types";
import "../styles/globals.css";

const ConnectingView: React.FC<{ platforms: Platform[] }> = ({ platforms }) => (
  <div className="flex flex-col items-center justify-center h-full gap-4 p-6">
    <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
    <div className="text-center">
      <p className="font-semibold text-gray-700">Connecting to {platforms.join(" & ")}</p>
      <p className="text-sm text-gray-500 mt-1">Complete authentication in the opened tab</p>
    </div>
  </div>
);

const Popup: React.FC = () => {
  const { currentView, setView, initialize, startAuth, setConsent, addConnectedPlatform, isLoading } = useAppStore();
  const [selectedPlatforms, setSelectedPlatforms] = React.useState<Platform[]>([]);
  const [authUrls, setAuthUrls] = React.useState<Record<Platform, string>>({} as Record<Platform, string>);

  useEffect(() => {
    initialize();

    // Listen for OAuth callback messages from background
    const handler = (message: { type: string; platform?: Platform; token?: string; userId?: string }) => {
      if (message.type === "OAUTH_SUCCESS" && message.platform && message.token && message.userId) {
        const { setAuthToken } = useAppStore.getState();
        setAuthToken(message.token, message.userId);
        addConnectedPlatform(message.platform);

        // Check if all platforms connected
        const { connectedPlatforms } = useAppStore.getState();
        const allConnected = selectedPlatforms.every((p) => connectedPlatforms.includes(p));
        if (allConnected || selectedPlatforms.length === 0) {
          setView("dashboard");
        }
      } else if (message.type === "AUTH_EXPIRED") {
        setView("platform-select");
      }
    };

    chrome.runtime.onMessage.addListener(handler);
    return () => chrome.runtime.onMessage.removeListener(handler);
  }, [selectedPlatforms]);

  const handlePlatformNext = (platforms: Platform[]) => {
    setSelectedPlatforms(platforms);
    setView("consent");
  };

  const handleConsentAgree = async (consent: ConsentData) => {
    setConsent(consent);
    try {
      const result = await startAuth(consent.platforms, consent.historical_allowed, consent.sync_allowed);
      setAuthUrls(result.auth_urls as Record<Platform, string>);
      setView("connecting");

      // Open auth URLs
      for (const [platform, url] of Object.entries(result.auth_urls)) {
        if (url) {
          chrome.tabs.create({ url, active: true });
          break; // Open one at a time
        }
      }
    } catch {
      // error already set in store
    }
  };

  return (
    <div className="w-80 h-[560px] bg-white flex flex-col overflow-hidden">
      {currentView === "platform-select" && (
        <PlatformSelector onNext={handlePlatformNext} />
      )}
      {currentView === "consent" && (
        <ConsentScreen
          platforms={selectedPlatforms}
          onAgree={handleConsentAgree}
          onBack={() => setView("platform-select")}
        />
      )}
      {currentView === "connecting" && (
        <ConnectingView platforms={selectedPlatforms} />
      )}
      {currentView === "dashboard" && <Dashboard />}
      {currentView === "settings" && <Settings />}
    </div>
  );
};

export default Popup;
