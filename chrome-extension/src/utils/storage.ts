import nacl from "tweetnacl";
import { encodeBase64, decodeBase64, encodeUTF8, decodeUTF8 } from "tweetnacl-util";
import { STORAGE_KEYS } from "../types";

const STORAGE_ENCRYPTION_KEY = "synapse_forgex_key_v1";

/**
 * Get or generate a persistent symmetric key stored in chrome.storage.local.
 */
async function getEncryptionKey(): Promise<Uint8Array> {
  return new Promise((resolve) => {
    chrome.storage.local.get(STORAGE_ENCRYPTION_KEY, (result) => {
      if (result[STORAGE_ENCRYPTION_KEY]) {
        resolve(decodeBase64(result[STORAGE_ENCRYPTION_KEY]));
      } else {
        const key = nacl.randomBytes(nacl.secretbox.keyLength);
        chrome.storage.local.set({ [STORAGE_ENCRYPTION_KEY]: encodeBase64(key) }, () => {
          resolve(key);
        });
      }
    });
  });
}

/**
 * Encrypt a string using TweetNaCl secretbox.
 */
export async function encryptData(data: string): Promise<string> {
  const key = await getEncryptionKey();
  const nonce = nacl.randomBytes(nacl.secretbox.nonceLength);
  const message = encodeUTF8(data);
  const box = nacl.secretbox(message, nonce, key);
  const combined = new Uint8Array(nonce.length + box.length);
  combined.set(nonce);
  combined.set(box, nonce.length);
  return encodeBase64(combined);
}

/**
 * Decrypt a string previously encrypted with encryptData.
 */
export async function decryptData(encrypted: string): Promise<string | null> {
  try {
    const key = await getEncryptionKey();
    const combined = decodeBase64(encrypted);
    const nonce = combined.slice(0, nacl.secretbox.nonceLength);
    const box = combined.slice(nacl.secretbox.nonceLength);
    const decrypted = nacl.secretbox.open(box, nonce, key);
    if (!decrypted) return null;
    return decodeUTF8(decrypted);
  } catch {
    return null;
  }
}

/**
 * Save the auth token encrypted to chrome.storage.local.
 */
export async function saveAuthToken(token: string): Promise<void> {
  const encrypted = await encryptData(token);
  return new Promise((resolve) => {
    chrome.storage.local.set({ [STORAGE_KEYS.AUTH_TOKEN]: encrypted }, resolve);
  });
}

/**
 * Load and decrypt the auth token from chrome.storage.local.
 */
export async function loadAuthToken(): Promise<string | null> {
  return new Promise((resolve) => {
    chrome.storage.local.get(STORAGE_KEYS.AUTH_TOKEN, async (result) => {
      const encrypted = result[STORAGE_KEYS.AUTH_TOKEN];
      if (!encrypted) return resolve(null);
      const token = await decryptData(encrypted);
      resolve(token);
    });
  });
}

/**
 * Save a plain value to chrome.storage.local.
 */
export function saveToStorage<T>(key: string, value: T): Promise<void> {
  return new Promise((resolve) => {
    chrome.storage.local.set({ [key]: value }, resolve);
  });
}

/**
 * Load a value from chrome.storage.local.
 */
export function loadFromStorage<T>(key: string): Promise<T | null> {
  return new Promise((resolve) => {
    chrome.storage.local.get(key, (result) => {
      resolve(result[key] ?? null);
    });
  });
}

/**
 * Remove a value from chrome.storage.local.
 */
export function removeFromStorage(key: string): Promise<void> {
  return new Promise((resolve) => {
    chrome.storage.local.remove(key, resolve);
  });
}

/**
 * Clear all Synapse ForgeX storage.
 */
export function clearAllStorage(): Promise<void> {
  return new Promise((resolve) => {
    chrome.storage.local.clear(resolve);
  });
}
