import discord
import re
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

YOUR_USER_ID = 195760464326688769

TRIGGERS = [
    "adventures continue is now under maintenance",
    "astro blasters is now under maintenance",
    "autopia is now under maintenance",
    "bayou adventure is now under maintenance",
    "car toon spin is now under maintenance",
    "sky school is now under maintenance",
    "incredicoaster is now under maintenance",
    "indiana jones™ adventure is now under maintenance",
    "haunted mansion is now under maintenance",
    "spider-man adventure is now under maintenance",
    "undersea adventure is now under maintenance",
    "mountain railroad is now under maintenance",
    "toy story midway mania! is now under maintenance",
    ("small world", "is now under maintenance"),
    "matterhorn bobsleds is now under maintenance",
    "mission: breakout! is now under maintenance",
    "runaway railway is now under maintenance",
    "smugglers run is now under maintenance",
    "space mountain is now under maintenance",
    "to the rescue! is now under maintenance",
    "radiator springs racers is now opened",
    "resistance is now opened",
]

def normalize(text):
    text = text.lower()
    text = re.sub(r"[''`]", "", text)           # apostrophes
    text = re.sub(r"[™®]", "", text)            # trademark symbols
    text = re.sub(r'[\"\"\u201c\u201d\u201e]', "", text)  # all quote variants
    text = re.sub(r'[^\w\s]', " ", text)        # replace any remaining punctuation with space
    text = re.sub(r'\s+', " ", text).strip()    # collapse multiple spaces
    return text

NORMALIZED_TRIGGERS = [normalize(t) for t in TRIGGERS]

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    normalized_msg = normalize(message.content)
    await message.channel.send(f"DEBUG: `{normalized_msg}`")

    for i, trigger in enumerate(TRIGGERS):
        if isinstance(trigger, tuple):
            matched = all(part in normalized_msg for part in trigger)
        else:
            matched = trigger in normalized_msg

        if matched:
            original = TRIGGERS[i]
            if isinstance(original, tuple):
                display = "Small world is now under maintenance"
            else:
                display = original[0].upper() + original[1:]
            await message.channel.send(f"<@{YOUR_USER_ID}> {display}")
            break

client.run(os.getenv("DISCORD_TOKEN"))
