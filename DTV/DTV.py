import sys
import os

os.system("@echo off & cls")
os.system("color 3")
os.system("title Discord Token Verifier / @DARKNOSY")

import discord
import aiohttp
import asyncio

TOKENS_FILE = "tokens.txt"  # Name of the text file containing Discord tokens

BADGE_NAMES = {
    1: "Discord Employee",
    2: "Partnered Server Owner",
    4: "HypeSquad Events",
    8: "Bug Hunter Level 1",
    64: "House Bravery",
    128: "House Brilliance",
    256: "House Balance",
    512: "Early Supporter",
    16384: "Bug Hunter Level 2",
    65536: "Verified Bot",
    131072: "Early Verified Bot Developer",
}

async def fetch_user_details(token):
    try:
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bot {token}" if token.startswith("Bot ") else token
            }

            # Fetch user data from Discord API
            async with session.get("https://discord.com/api/v10/users/@me", headers=headers) as response:
                if response.status == 200:
                    user_data = await response.json()

                    avatar_url = f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png" if user_data["avatar"] else "No avatar"

                    details = {
                        "Token": token,
                        "Username": user_data["username"],
                        "User ID": user_data["id"],
                        "Discriminator": user_data["discriminator"],
                        "Avatar URL": avatar_url,
                        "Bot": user_data.get("bot", False),
                        "Badges": user_data.get("public_flags", 0),
                        "Bio": user_data.get("bio", "No bio"),
                    }

                    return details
                else:
                    return None

    except discord.errors.LoginFailure:
        return None

async def main():
    with open(TOKENS_FILE, "r") as file:
        tokens = file.read().splitlines()

    tasks = [fetch_user_details(token) for token in tokens]
    results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            print("Token Details:")
            for key, value in result.items():
                if key == "Badges":
                    print("Badges:")
                    badges = value
                    for badge_value, badge_name in BADGE_NAMES.items():
                        if badge_value & badges == badge_value:
                            print(f"- {badge_name}")
                else:
                    print(f"{key}: {value}")
            print("------------------------")
        else:
            print("Invalid token")
            print("------------------------")

asyncio.run(main())
os.system("pause")
