// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "createDoc") {
    handleDocCreation(request.title, request.html)
      .then((url) => {
        sendResponse({ success: true, url: url });
      })
      .catch((err) => {
        console.error("Doc creation error: ", err);
        sendResponse({ success: false, error: err.message });
      });
    return true;
  }
});

// MUST be a "Web application" OAuth client, NOT a "Chrome Extension" client.
// Chrome Extension clients only accept the chrome-extension:// redirect used by
// getAuthToken(); launchWebAuthFlow() redirects to .chromiumapp.org, which can
// only be registered on a Web application client.
// This is the "gemini canvas" Web application client, which has
//   https://mldaenkgmbajbpepfiegdjgnbedkiilf.chromiumapp.org/
// registered as an authorized redirect URI. Do not swap this back to the
// "gemini latex" Chrome Extension client (...-78kr...) — that one 400s with
// redirect_uri_mismatch because it cannot register a .chromiumapp.org URI.
const GOOGLE_CLIENT_ID = "130646946045-57merovpbkrq3anmuptt6daebo28u39h.apps.googleusercontent.com";

const SCOPE = 'https://www.googleapis.com/auth/drive.file';
const TOKEN_CACHE_KEY = 'oauthToken';

// Run the implicit flow once. When interactive is false we add prompt=none, so
// Google either returns a token immediately (existing session + existing grant)
// or errors out without ever showing UI.
function launchFlow(interactive) {
  const redirectUri = chrome.identity.getRedirectURL();
  const params = new URLSearchParams({
    client_id: GOOGLE_CLIENT_ID,
    response_type: 'token',
    redirect_uri: redirectUri,
    scope: SCOPE
  });
  if (!interactive) params.set('prompt', 'none');

  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;

  return new Promise((resolve, reject) => {
    chrome.identity.launchWebAuthFlow({ url: authUrl, interactive }, (redirectUrl) => {
      if (chrome.runtime.lastError || !redirectUrl) {
        const msg = chrome.runtime.lastError
          ? chrome.runtime.lastError.message
          : "No redirect URL returned.";
        reject(new Error(msg));
        return;
      }

      // Token comes back in the hash fragment (#access_token=...&expires_in=...)
      const hash = new URLSearchParams(new URL(redirectUrl).hash.substring(1));
      const token = hash.get('access_token');
      if (!token) {
        reject(new Error(hash.get('error') || "Access token was not returned by Google."));
        return;
      }

      // expires_in is seconds; keep a 60s safety margin so we never send a
      // token that expires mid-flight.
      const expiresIn = parseInt(hash.get('expires_in') || '3600', 10);
      resolve({ token, expiresAt: Date.now() + (expiresIn - 60) * 1000 });
    });
  });
}

// Cached token -> silent re-auth -> interactive sign-in. Only the last one
// shows a window, and it should be rare.
async function getAuthToken(forceRefresh = false) {
  if (!forceRefresh) {
    const cached = (await chrome.storage.session.get(TOKEN_CACHE_KEY))[TOKEN_CACHE_KEY];
    if (cached && cached.expiresAt > Date.now()) {
      return cached.token;
    }
  }

  let result;
  try {
    result = await launchFlow(false);
  } catch (silentErr) {
    console.log("[OAuth] Silent refresh unavailable, prompting:", silentErr.message);
    result = await launchFlow(true);
  }

  await chrome.storage.session.set({ [TOKEN_CACHE_KEY]: result });
  return result.token;
}

async function handleDocCreation(title, html) {
  let response = await uploadDoc(await getAuthToken(), title, html);

  // A cached token can be revoked server-side before its stated expiry.
  // Drop it and do one clean retry rather than surfacing a confusing 401.
  if (response.status === 401) {
    await chrome.storage.session.remove(TOKEN_CACHE_KEY);
    response = await uploadDoc(await getAuthToken(true), title, html);
  }

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Drive API error: ${response.status} - ${errText}`);
  }

  const fileData = await response.json();
  const docUrl = `https://docs.google.com/document/d/${fileData.id}/edit`;

  await chrome.tabs.create({ url: docUrl });

  return docUrl;
}

async function uploadDoc(token, title, html) {
  const boundary = '-------314159265358979323846';
  const delimiter = "\r\n--" + boundary + "\r\n";
  const closeDelimiter = "\r\n--" + boundary + "--";

  const metadata = {
    name: title,
    mimeType: 'application/vnd.google-apps.document'
  };

  const multipartRequestBody =
    delimiter +
    'Content-Type: application/json; charset=UTF-8\r\n\r\n' +
    JSON.stringify(metadata) +
    delimiter +
    'Content-Type: text/html; charset=UTF-8\r\n\r\n' +
    `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>${html}</body></html>` +
    closeDelimiter;

  return fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'multipart/related; boundary=' + boundary
    },
    body: multipartRequestBody
  });
}
