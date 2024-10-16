from telethon import TelegramClient, events, Button
from telethon.tl.types import PeerChannel, Channel

# Replace with your actual API ID, Hash, and Bot Token
api_id = '23748760'  # Example: '123456'
api_hash = '5350341c03ca519c0945a02d8a6c8036'  # Example: 'abcdef1234567890abcdef1234567890'
bot_token = '7475923472:AAGI5k2w-KglPQiTLQqe1VWrysmVtnSdHIk'  # Example: '123456789:ABCdefGHIjklmnopQRStuvWXYZ'

# Create the bot client
client = TelegramClient('GU_Noobieshop_bot', api_id, api_hash).start(bot_token=bot_token)

# Set the passwords
BOT_PASSWORDS = ['@Antor1040', '@NoobieNoiso', '@RionMental26']  # List of passwords

# Dictionary to store which users have unlocked the bot
unlocked_users = {}

# Start event handler
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond(
        "Welcome to GU_Noobieshop Bot! Please get the password from the admin:\n"
        "Contact Support: [Noobie Support](https://t.me/NoobieXNoiso)\n"
        "Join our Channel: [Noobie Channel](https://t.me/NoobieShopp)",
        parse_mode='markdown'
    )

# Unlock button handler
@client.on(events.CallbackQuery(data=b'unlock'))
async def ask_password(event):
    await event.respond(
        "Please enter the password to unlock the bot:",
        buttons=[[Button.inline('Cancel', b'cancel')]]
    )

# Password entry handler
@client.on(events.NewMessage)
async def check_password(event):
    user_id = event.sender_id

    # If the user has already unlocked the bot
    if unlocked_users.get(user_id):
        await event.respond("Please enter the group URL to fetch usernames.")
        return

    # If the user enters the correct password
    if event.text in BOT_PASSWORDS:
        unlocked_users[user_id] = True
        await event.respond(
            "✅ Bot unlocked successfully! Please enter the group or channel URL to fetch usernames:"
        )
    else:
        await event.respond("Please try again or press 'Cancel'.")

# Cancel button handler
@client.on(events.CallbackQuery(data=b'cancel'))
async def cancel(event):
    await event.respond("Action cancelled. Type /start to try again.")

# Fetch Usernames from Group or Channel
@client.on(events.NewMessage)
async def fetch_usernames(event):
    user_id = event.sender_id

    if unlocked_users.get(user_id):
        group_url = event.text.strip()

        # Attempt to resolve the group URL to a username or ID
        try:
            group = await client.get_entity(group_url)
            if isinstance(group, (PeerChannel, Channel)):
                usernames = []
                async for member in client.iter_participants(group):
                    if member.username:
                        usernames.append(f"@{member.username}")  # Format as @username

                # Check if usernames list is empty
                if usernames:
                    await send_long_message(event, "Usernames:\n" + "\n".join(usernames))
                else:
                    await event.respond("No usernames found in this group or channel.")
            else:
                await event.respond("The provided link is not a valid group or channel URL.")
        except Exception:
            # Do not provide a specific error message
            await event.respond("Please check the group/channel link.")
    else:
        await event.respond("Please unlock the bot first by typing /start.")

# Function to send long messages in chunks
async def send_long_message(event, message):
    max_length = 4096
    for i in range(0, len(message), max_length):
        await event.respond(message[i:i + max_length])

# Run the bot
if __name__ == "__main__":
    client.run_until_disconnected()
