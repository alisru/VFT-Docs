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

// We will replace this Client ID string once you provide the new Web Application Client ID
const GOOGLE_CLIENT_ID = "130646946045-78krafccvuidslabotp03v2s92st2u4k.apps.googleusercontent.com";

async function getAuthToken() {
  const redirectUri = chrome.identity.getRedirectURL();
  const scope = encodeURIComponent('https://www.googleapis.com/auth/drive.file');
  
  console.log("[OAuth Debug] Client ID:", GOOGLE_CLIENT_ID);
  console.log("[OAuth Debug] Generated Redirect URI:", redirectUri);
  
  // Construct the Google OAuth 2.0 Web Auth URL
  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&response_type=token&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scope}`;
  console.log("[OAuth Debug] Full Auth URL:", authUrl);

  return new Promise((resolve, reject) => {
    // Launch standard web authorization flow (Brave compatible)
    chrome.identity.launchWebAuthFlow({
      url: authUrl,
      interactive: true
    }, function(redirectUrl) {
      if (chrome.runtime.lastError) {
        reject(new Error(chrome.runtime.lastError.message));
        return;
      }
      
      if (!redirectUrl) {
        reject(new Error("Authorization failed. No redirect URL returned."));
        return;
      }
      
      try {
        // Extract access_token from the URL hash fragment (#access_token=...)
        const url = new URL(redirectUrl);
        const params = new URLSearchParams(url.hash.substring(1));
        const token = params.get('access_token');
        
        if (token) {
          resolve(token);
        } else {
          reject(new Error("Access token was not returned by Google."));
        }
      } catch (err) {
        reject(new Error("Failed to parse redirect URL: " + err.message));
      }
    });
  });
}

async function handleDocCreation(title, html) {
  const token = await getAuthToken();

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

  const response = await fetch('https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + token,
      'Content-Type': 'multipart/related; boundary=' + boundary
    },
    body: multipartRequestBody
  });

  if (!response.ok) {
    const errText = await response.text();
    throw new Error(`Drive API error: ${response.status} - ${errText}`);
  }

  const fileData = await response.json();
  const fileId = fileData.id;
  
  const docUrl = `https://docs.google.com/document/d/${fileId}/edit`;
  
  await chrome.tabs.create({ url: docUrl });

  return docUrl;
}
