import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="Spooky Game"))

# Load all cogs from the cogs directory
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename}')
# Run bot with async setup
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

# Run the bot
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
