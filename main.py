
import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def encurtar_link(url):
    api_url = f"https://is.gd/create.php?format=simple&url={url}"
    r = requests.get(api_url)
    return r.text

@bot.event
async def on_ready():
    print(f"✅ Bot online como {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="hidelink", description="Transforma seu link em markdown oculto")
@app_commands.describe(url="O link que você quer esconder")
async def hidelink(interaction: discord.Interaction, url: str):
    if not url:
        await interaction.response.send_message("❌ Você precisa colocar um URL!", ephemeral=True)
        return
    try:
        short_url = encurtar_link(url)
        resultado = f"[{url}]({short_url})"
        await interaction.response.send_message(resultado)
    except Exception as e:
        await interaction.response.send_message(f"❌ Erro ao processar o link: {e}", ephemeral=True)

bot.run(os.getenv("BOT_TOKEN"))
