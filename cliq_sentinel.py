import urllib.request, urllib.parse, json
import time, os

AUTH_FILE = "/home/warwick/.openclaw/workspace/cliq_auth.json"
CHANNELS_FILE = "/home/warwick/.openclaw/workspace/cliq_channels.json"
STATE_FILE = "/home/warwick/.openclaw/workspace/cliq_state.json"

def get_token():
    with open(AUTH_FILE, "r") as f:
        auth = json.load(f)
    req = urllib.request.Request("https://accounts.zoho.com.au/oauth/v2/token", data=urllib.parse.urlencode({
        "grant_type": "refresh_token", "client_id": auth["client_id"],
        "client_secret": auth["client_secret"], "refresh_token": auth["refresh_token"]
    }).encode(), method="POST")
    res = json.loads(urllib.request.urlopen(req).read().decode())
    return res["access_token"]

def poll_channels():
    token = get_token()
    with open(CHANNELS_FILE, "r") as f:
        channels = json.load(f)
    
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    for name, uid in channels.items():
        if not uid: continue
        url = f"https://cliq.zoho.com.au/api/v2/channels/{uid}/messages?limit=10"
        req = urllib.request.Request(url, headers=headers)
        try:
            res = json.loads(urllib.request.urlopen(req).read().decode())
            messages = res.get("data", [])
            for msg in messages:
                msg_id = msg.get("id")
                sender = msg.get("sender", {}).get("name", "Unknown")
                text = msg.get("content", "")
                
                if msg_id not in state:
                    state[msg_id] = True
                    # Check for keywords
                    if "warwick" in text.lower() or "approve" in text.lower() or "budget" in text.lower() or "thoughts" in text.lower() or "?" in text:
                        print(f"🚨 ALERT from {name} | {sender}: {text}")
        except Exception as e:
            print(f"Error polling {name}: {e}")

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

if __name__ == "__main__":
    while True:
        poll_channels()
        time.sleep(60)