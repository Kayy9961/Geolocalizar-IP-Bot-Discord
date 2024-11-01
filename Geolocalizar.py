import discord
from discord.ext import commands
from discord import app_commands
import requests
import re

intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='!', intents=intents)

class IPCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def validar_ip(self, ip):
        patron = re.compile(r"""
            ^
            (?:
              (?:
                (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
                \.
              ){3}
              (?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)
            )
            $
        """, re.VERBOSE)
        return patron.match(ip) is not None

    def obtener_info_ip(self, ip):
        try:
            respuesta = requests.get(f"http://ip-api.com/json/{ip}")
            datos = respuesta.json()
            
            if datos['status'] == 'success':
                embed = discord.Embed(title=f"Información de la IP: {ip}", color=0x00ff00)
                embed.add_field(name="País", value=datos.get('country', 'N/A'), inline=True)
                embed.add_field(name="Región", value=datos.get('regionName', 'N/A'), inline=True)
                embed.add_field(name="Ciudad", value=datos.get('city', 'N/A'), inline=True)
                embed.add_field(name="Código Postal", value=datos.get('zip', 'N/A'), inline=True)
                embed.add_field(name="ISP", value=datos.get('isp', 'N/A'), inline=True)
                embed.add_field(name="Organización", value=datos.get('org', 'N/A'), inline=True)
                embed.add_field(name="AS", value=datos.get('as', 'N/A'), inline=True)
                embed.set_footer(text="Bot Created By Kayy")
                return embed
            else:
                return f"⚠️ **Error:** {datos.get('message', 'No se pudo obtener la información de la IP.')}"
        except requests.exceptions.RequestException as e:
            return f"⚠️ **Error al realizar la solicitud:** {e}"

    @app_commands.command(name="ip", description="Obtiene información sobre una dirección IP")
    async def ip(self, interaction: discord.Interaction, direccion_ip: str):
        """Obtiene información detallada de una dirección IP proporcionada."""
        await interaction.response.defer()

        ip = direccion_ip.strip()
        if self.validar_ip(ip):
            info = self.obtener_info_ip(ip)
            if isinstance(info, discord.Embed):
                await interaction.followup.send(embed=info)
            else:
                await interaction.followup.send(info)
        else:
            await interaction.followup.send("⚠️ La dirección IP introducida no es válida", ephemeral=True)

@bot.event
async def on_ready():
    await bot.add_cog(IPCommands(bot))
    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar comandos: {e}")
    print(f'Bot conectado como {bot.user}')

bot.run('EL TOKEN DE TU BOT DE DISCORD')
