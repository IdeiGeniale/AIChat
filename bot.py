import discord
from google import genai
from google.genai import types
import os
from flask import Flask
from threading import Thread

# 1. Setup a dummy web server for Render health checks
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# 2. Initialize the Gemini Client
ai_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# 3. Initialize Discord Bot (Requires Guilds, Messages, and Message Content intents)
intents = discord.Intents.default()
intents.message_content = True
discord_client = discord.Client(intents=intents)

@discord_client.event
async def on_ready():
    print(f'Bot is online as {discord_client.user}')

@discord_client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == discord_client.user:
        return

    # Trigger conditions: Responds to Direct Messages (DMs) OR when the bot is explicitly tagged
    is_dm = isinstance(message.channel, discord.DMChannel)
    is_mentioned = discord_client.user in message.mentions

    if is_dm or is_mentioned:
        # Clean up the prompt by removing the bot mention syntax if present
        user_prompt = message.content.replace(f'<@{discord_client.user.id}>', '').strip()
        
        # If there's no text but there is an attachment, give Gemini a default prompt
        if not user_prompt and message.attachments:
            user_prompt = "Describe this image or document."

        async with message.channel.typing():
            try:
                # Prepare the contents payload for Gemini
                contents_payload = [user_prompt]

                # Process any attachments (Images, PDFs, etc.)
                for attachment in message.attachments:
                    # Download the file into memory as bytes
                    file_bytes = await attachment.read()
                    
                    # Wrap it in the SDK's Part objects
                    image_part = types.Part.from_bytes(
                        data=file_bytes,
                        mime_type=attachment.content_type,
                    )
                    contents_payload.append(image_part)

                # Generate content using the prepared payload
                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents_payload,
                )
                
                # Discord has a 2000-character limit per message
                if len(response.text) > 2000:
                    for i in range(0, len(response.text), 2000):
                        await message.channel.send(response.text[i:i+2000])
                else:
                    await message.channel.send(response.text)

            except Exception as e:
                await message.channel.send("An error occurred while processing your request.")
                print(f"Error: {e}")

# 4. Start the web server and the Discord bot
if __name__ == "__main__":
    keep_alive()
    discord_client.run(os.environ.get("DISCORD_TOKEN"))
