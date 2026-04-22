// Background Service Worker (Manifest V3)
// Handles OAuth callback tab detection and lifecycle management

const OAUTH_CALLBACK_PATTERNS = [
  "http://localhost:8000/api/auth/youtube/callback*",
  "http://localhost:8000/api/auth/reddit/callback*",
];

// Listen for tab URL changes to detect OAuth callbacks
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status !== "complete" || !tab.url) return;

  const url = new URL(tab.url);

  // Detect YouTube callback
  if (url.pathname === "/api/auth/youtube/callback") {
    const token = url.searchParams.get("token");
    const userId = url.searchParams.get("user_id");
    if (token && userId) {
      chrome.runtime.sendMessage({ type: "OAUTH_SUCCESS", platform: "youtube", token, userId });
      chrome.tabs.remove(tabId);
    } else {
      // If callback hit the backend successfully, check for token via API response
      fetchTokenFromCallback(tabId, url, "youtube");
    }
    return;
  }

  // Detect Reddit callback
  if (url.pathname === "/api/auth/reddit/callback") {
    const token = url.searchParams.get("token");
    const userId = url.searchParams.get("user_id");
    if (token && userId) {
      chrome.runtime.sendMessage({ type: "OAUTH_SUCCESS", platform: "reddit", token, userId });
      chrome.tabs.remove(tabId);
    } else {
      fetchTokenFromCallback(tabId, url, "reddit");
    }
    return;
  }
});

async function fetchTokenFromCallback(tabId: number, callbackUrl: URL, platform: string): Promise<void> {
  const code = callbackUrl.searchParams.get("code");
  const state = callbackUrl.searchParams.get("state");
  if (!code || !state) return;

  try {
    const response = await fetch(
      `http://localhost:8000/api/auth/${platform}/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state)}`
    );
    if (response.ok) {
      const data = await response.json();
      chrome.runtime.sendMessage({
        type: "OAUTH_SUCCESS",
        platform,
        token: data.token,
        userId: data.user_id,
      });
      chrome.tabs.remove(tabId);
    }
  } catch (err) {
    console.error("OAuth callback error:", err);
  }
}

// Handle extension install/update
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === "install") {
    console.log("Synapse ForgeX installed");
    chrome.tabs.create({ url: chrome.runtime.getURL("options.html") });
  }
});

// Handle messages from popup/content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "GET_TAB_URL") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      sendResponse({ url: tabs[0]?.url || "" });
    });
    return true;
  }
  if (message.type === "OPEN_DASHBOARD") {
    chrome.tabs.create({ url: chrome.runtime.getURL("dashboard.html") });
  }
});

export {};
