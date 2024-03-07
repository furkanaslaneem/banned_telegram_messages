from telethon.sync import TelegramClient
import time

api_id = '22750064'
api_hash = 'bad926f0bcaa010fac4823630d26ca74'
phone_number = 'enter your phone number'

# Sign in with Telegram API
client = TelegramClient('session_name', api_id, api_hash)
client.start()  # Start session

# If not logged in, verify with phone number
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, input('Enter the verification code:'))

# Targeted group chat ID (chat ID)
destination_group = -1002012745458  # For example, the chat ID of the targeted group

# Chat IDs of source channels
source_channels = [-1101475050530]  # For example, the chat IDs of the source channels

latest_message_ids = {source: None for source in source_channels}
sent_messages = set()

while True:
    for source in source_channels:
        try:
            # Get the channel's latest message
            messages = client.get_messages(source, limit=1)

            if messages and messages[0].id != latest_message_ids[source] and messages[0].id not in sent_messages:
                # There is a new message and it has not been sent before
                latest_message_ids[source] = messages[0].id

                if messages[0].text:
                    # Send the message directly to the target group (prefixed with "BOT MESSAGE")
                    bot_message = f" BOT MESSAGE: \n{messages[0].text}"
                    client.send_message(destination_group, bot_message)
                elif messages[0].media:
                    # If media file is available, receive and send media
                    client.send_message(destination_group, file=messages[0].media)

                sent_messages.add(messages[0].id)
        except Exception as e:
            print(f"Error: {e}")
            continue

    # Wait for a certain period of time and check again
    time.sleep(5)  # For example, you can wait 5 seconds
