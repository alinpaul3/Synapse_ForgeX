// Content Script
// Runs on YouTube and Reddit pages for any needed page-level interaction

const hostname = window.location.hostname;

function notifyPageLoad(): void {
  chrome.runtime.sendMessage({
    type: "PAGE_LOADED",
    url: window.location.href,
    platform: hostname.includes("youtube") ? "youtube" : "reddit",
  }).catch(() => {
    // Extension context may be invalidated, ignore
  });
}

// Notify background of page load
notifyPageLoad();

export {};
