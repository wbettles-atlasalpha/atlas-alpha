import requests
import datetime
import json

# Zoho API credentials
token = "your_zoho_auth_token"
cliq_headers = {
    'Authorization': f'Zoho-oauthtoken {token}'
}

# WhatsApp integration (for sending alerts)
whatsapp_api_url = 'https://api.yourwhatsappintegration.com/send'
whatsapp_headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer your_whatsapp_api_key'}

# List of channels to check
def get_all_channels():
    url = "https://cliq.zoho.com/api/v2/channels"
    response = requests.get(url, headers=cliq_headers)
    return response.json().get('data', [])

# Fetch messages from a specific channel within the last week
def fetch_messages(channel_id):
    one_week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    url = f"https://cliq.zoho.com/api/v2/channels/{channel_id}/messages?from={one_week_ago}"
    response = requests.get(url, headers=cliq_headers)
    return response.json().get('data', [])

# Check if Warwick is mentioned in a message
def warwick_mentioned(message):
    return 'Warwick' in message.get('text', '')

# Check if a message requires action
def requires_action(message):
    triggers = ['approve', 'budget', '?', 'action needed', 'please respond']  # Add more as necessary
    return any(trigger in message.get('text', '').lower() for trigger in triggers)

# Send a WhatsApp alert
def send_whatsapp_alert(channel, messages):
    text = f"Important messages in {channel}:\n" + "\n".join([f"- {msg['text']}" for msg in messages])
    data = {
        'phone': 'your_whatsapp_number',
        'body': text
    }
    # Send the alert
    requests.post(whatsapp_api_url, headers=whatsapp_headers, data=json.dumps(data))

# Main function to gather and process mentions
def process_mentions():
    mentions_summary = ""
    channels = get_all_channels()
    for channel in channels:
        messages = fetch_messages(channel['id'])
        channel_mentions = [msg for msg in messages if warwick_mentioned(msg)]
        important_messages = [msg for msg in channel_mentions if requires_action(msg)]
        # Send important messages immediately
        if important_messages:
            send_whatsapp_alert(channel['name'], important_messages)
        # Aggregate non-important messages for summary
        non_important = [msg for msg in channel_mentions if msg not in important_messages]
        if non_important:
            mentions_summary += f"Non-important mentions in {channel['name']}: {len(non_important)}\n"

    # Send non-important summary
    if mentions_summary:
        data = {
            'phone': 'your_whatsapp_number',
            'body': mentions_summary
        }
        requests.post(whatsapp_api_url, headers=whatsapp_headers, data=json.dumps(data))

# Run the process
def main():
    process_mentions()

if __name__ == '__main__':
    main()