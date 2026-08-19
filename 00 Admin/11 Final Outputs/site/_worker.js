/**
 * Password gate for the Tap That Brewery 3D Process delivery pack.
 *
 * Soft gate only — the password is shared with the client and is not protecting
 * secrets. It keeps the pack off search engines and away from casual visitors.
 * Set PACK_PASSWORD as a Pages environment variable to override the default.
 */

const DEFAULT_PASSWORD = "tapthat2026";
const COOKIE = "tt_session";
const MAX_AGE = 60 * 60 * 24 * 7; // 7 days

const enc = new TextEncoder();

async function hmac(key, message) {
  const cryptoKey = await crypto.subtle.importKey(
    "raw", enc.encode(key), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", cryptoKey, enc.encode(message));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

async function mintToken(password) {
  const expiry = Math.floor(Date.now() / 1000) + MAX_AGE;
  return `${expiry}.${await hmac(password, String(expiry))}`;
}

async function tokenValid(token, password) {
  if (!token || !token.includes(".")) return false;
  const [expiry, sig] = token.split(".");
  if (!/^\d+$/.test(expiry) || Number(expiry) < Math.floor(Date.now() / 1000)) return false;
  return timingSafeEqual(sig || "", await hmac(password, expiry));
}

function readCookie(request, name) {
  const header = request.headers.get("Cookie") || "";
  for (const part of header.split(";")) {
    const [k, ...v] = part.trim().split("=");
    if (k === name) return v.join("=");
  }
  return null;
}

function safeNext(raw) {
  // Only allow same-origin absolute paths — never an open redirect.
  return raw && raw.startsWith("/") && !raw.startsWith("//") ? raw : "/";
}

function gate({ next = "/", error = false } = {}) {
  const body = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Tap That Brewery</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=Karla:wght@400;500&family=IBM+Plex+Mono:wght@400&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;color:#F7F3EA;
    font-family:'Karla',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
    background:radial-gradient(120% 120% at 50% 0%,#1D4726 0%,#14361D 45%,#081C10 100%)}
  .card{width:100%;max-width:392px;text-align:center}
  .badge{width:200px;height:auto;display:block;margin:0 auto 24px}
  h1{font-family:'Archivo',sans-serif;font-weight:700;margin:0 0 8px;font-size:30px;letter-spacing:-.02em}
  p.sub{opacity:.75;margin:0 0 24px;font-size:15px;line-height:1.6}
  p.err{background:rgba(210,164,90,.16);border:1px solid rgba(210,164,90,.55);
    border-radius:5px;padding:10px 12px;margin:0 0 14px;font-size:14px}
  form{display:flex;flex-direction:column;gap:12px}
  input{padding:13px 14px;border-radius:5px;border:1px solid rgba(247,243,234,.28);
    background:rgba(247,243,234,.10);color:#F7F3EA;font-size:16px;font-family:inherit}
  input::placeholder{color:rgba(247,243,234,.55)}
  input:focus{outline:none;border-color:#CE9A49;background:rgba(247,243,234,.16)}
  button{padding:13px 14px;border-radius:4px;border:0;background:#B07C2E;color:#081C10;
    font-family:'Archivo',sans-serif;font-size:16px;font-weight:700;cursor:pointer;letter-spacing:.01em}
  button:hover{background:#CE9A49}
  button:focus-visible{outline:2px solid #F7F3EA;outline-offset:2px}
  .foot{font-family:'IBM Plex Mono',monospace;opacity:.5;font-size:11px;margin-top:22px;
    text-transform:uppercase;letter-spacing:.14em}
</style>
</head>
<body>
  <main class="card">
    <img class="badge" src="/brand/tapthat-badge.png" alt="Tap That Brewery" width="200" height="134">
    <h1>Your 3D Process.</h1>
    <p class="sub">This pack is private. Enter the password to continue.</p>
    ${error ? '<p class="err">That password did not match. Try again.</p>' : ""}
    <form method="POST" action="/__auth">
      <input type="hidden" name="next" value="${next.replace(/"/g, "&quot;")}">
      <input type="password" name="password" placeholder="Password" autofocus
             autocomplete="current-password" aria-label="Password" required>
      <button type="submit">View the pack</button>
    </form>
    <p class="foot">Jewell Projects</p>
  </main>
</body>
</html>`;
  return new Response(body, {
    status: error ? 401 : 401,
    headers: {
      "content-type": "text/html; charset=UTF-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow, noarchive, nosnippet",
      "x-content-type-options": "nosniff",
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const password = (env && env.PACK_PASSWORD) || DEFAULT_PASSWORD;

    if (url.pathname === "/__auth") {
      if (request.method !== "POST") return new Response("Method not allowed", { status: 405 });
      const form = await request.formData();
      const next = safeNext(form.get("next"));
      if (form.get("password") !== password) return gate({ next, error: true });
      return new Response(null, {
        status: 303,
        headers: {
          location: next,
          "set-cookie": `${COOKIE}=${await mintToken(password)}; Path=/; Max-Age=${MAX_AGE}; HttpOnly; Secure; SameSite=Lax`,
          "cache-control": "no-store",
        },
      });
    }

    if (url.pathname === "/__signout") {
      return new Response(null, {
        status: 303,
        headers: {
          location: "/",
          "set-cookie": `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`,
        },
      });
    }

    // Brand assets stay public: the gate page itself needs the logo, and these
    // are the same files already served from the client's public website.
    const isBrandAsset = url.pathname.startsWith("/brand/");

    if (!isBrandAsset && !(await tokenValid(readCookie(request, COOKIE), password))) {
      return gate({ next: url.pathname + url.search });
    }

    const response = await env.ASSETS.fetch(request);
    const headers = new Headers(response.headers);
    headers.set("x-robots-tag", "noindex, nofollow, noarchive, nosnippet");
    headers.set("cache-control", "no-store");
    return new Response(response.body, { status: response.status, headers });
  },
};
