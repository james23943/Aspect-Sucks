import discord
from discord.ext import commands
import asyncio
from discord import app_commands

class SpaceShooter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games = {}

    @app_commands.command(name="play", description="Start a new space shooter game session")
    async def play(self, interaction: discord.Interaction):
        player = interaction.user
        
        game_embed = discord.Embed(
            title="🎮 Space Shooter",
            description="Use the buttons to move. Reach the green safe zone while avoiding the red enemy!",
            color=discord.Color.blue()
        )
        
        # Create game controls
        controls = discord.ui.View(timeout=60)
        
        async def move_button_callback(b_interaction, direction):
            if b_interaction.user != player:
                return
            await b_interaction.response.send_message(f"Moved {direction}", ephemeral=True)
            
        buttons = {
            "⬆️": "up",
            "⬇️": "down",
            "⬅️": "left",
            "➡️": "right"
        }
        
        for emoji, direction in buttons.items():
            button = discord.ui.Button(style=discord.ButtonStyle.secondary, emoji=emoji)
            button.callback = lambda b_i, d=direction: move_button_callback(b_i, d)
            controls.add_item(button)

        # Game board representation using emojis
        game_state = [
            "⬛⬛⬛⬛⬛",
            "⬛🔴⬛⬛⬛",
            "⬛⬛⚪⬛⬛",
            "⬛⬛⬛⬛🟩"
        ]
        
        game_embed.add_field(name="Game Board", value="\n".join(game_state), inline=False)
        
        await interaction.response.send_message(embed=game_embed, view=controls)
        
        self.games[player.id] = {
            "board": game_state,
            "position": [2, 2],
            "enemy_pos": [1, 1]
        }

    @app_commands.command(name="stop", description="Stop your current game session")
    async def stop(self, interaction: discord.Interaction):
        if interaction.user.id in self.games:
            del self.games[interaction.user.id]
            await interaction.response.send_message("Game session ended!", ephemeral=True)
        else:
            await interaction.response.send_message("No active game session found.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SpaceShooter(bot))
