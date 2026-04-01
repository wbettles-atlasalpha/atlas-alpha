import urllib.request, urllib.parse, json, os
import requests

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

def main():
    token = get_token()
    with open(CHANNELS_FILE, "r") as f:
        channels = json.load(f)
    
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)

    headers = {"Authorization": f"Zoho-oauthtoken {token}"}
    alerts = []
    
    for name, uid in channels.items():
        if not uid: continue
        url = f"https://cliq.zoho.com.au/api/v2/channels/{uid}/messages?limit=10"
        req = urllib.request.Request(url, headers=headers)
        try:
            res = json.loads(urllib.request.urlopen(req).read().decode())
            messages = res.get("data", [])
            
            for msg in reversed(messages): # oldest to newest
                msg_id = msg.get("id")
                sender_name = msg.get("sender", {}).get("name", "Unknown")
                sender_id = msg.get("sender", {}).get("id")
                text = msg.get("content", "")
                
                if msg_id not in state:
                    state[msg_id] = True
                    # Skip our own messages
                    if sender_name == "Warwick":
                        continue
                    
                    text_lower = text.lower()
                    if "warwick" in text_lower or "@warwick" in text_lower or "?" in text_lower or "approve" in text_lower or "budget" in text_lower:
                        alerts.append(f"🚨 **Cliq Alert ({name})**\n{sender_name} said: \"{text}\"\n")
        except Exception as e:
            pass

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
        
    if alerts:
        message({"action": "send", "channel": "whatsapp", "target": "+61481879871", "message": "\n".join(alerts)})
    else:
        print("NO_ALERTS")

if __name__ == "__main__":
    main()