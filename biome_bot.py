import discord
from discord.ext import commands

TOKEN = 'MTU0OTk0MTcxMTYyMTQ1NTkyMg.GsW3wv.GdK8CLzdeVQQijHixc8WgnarElwvSUIqqZrrqo'

# 1. CANALES DE DESTINO PARA BIOMAS RAROS
BIOMES_RAROS = {
    "dreamspace": 1549937750638075995,  # ID del canal #dreamspace
    "glitched":   1549943866109595708,  # ID del canal #glitched
    "cyberspace": 1549943902675542137,  # ID del canal #cyberspace
    "singularity": 1549943953892311140  # ID del canal #singularity
}

# 2. CANAL DE DESTINO PARA BIOMAS NORMALES
CANAL_BIOMAS_NORMALES = 1549934620320071700  # ID del canal #biomas-normales

# 3. UNICO CANAL DE ORIGEN (Donde envía la macro)
CANAL_LOGS_UNICO = 1549939549151563858  # ID del canal de logs principal

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    # Ignorar mensajes del propio bot
    if message.author == bot.user:
        return

    # Escuchar SOLO en el canal de logs único
    if message.channel.id == CANAL_LOGS_UNICO:
        texto_analizar = message.content.lower()

        # Extraer el texto de los Embeds de SolRich
        for embed in message.embeds:
            if embed.title:
                texto_analizar += " " + embed.title.lower()
            if embed.description:
                texto_analizar += " " + embed.description.lower()
            for field in embed.fields:
                texto_analizar += f" {field.name.lower()} {field.value.lower()}"

        es_raro = False

        # Comprobar si es un bioma raro
        for bioma_raro, channel_id in BIOMES_RAROS.items():
            if bioma_raro in texto_analizar:
                es_raro = True
                canal_raro = bot.get_channel(channel_id)
                if canal_raro:
                    await canal_raro.send(
                        content=f"🚨 **¡BIOMA RARO DETECTADO: {bioma_raro.upper()}!** 🚨\n@everyone",
                        embeds=message.embeds if message.embeds else None
                    )
                break

        # Si no es raro, lo manda a "biomas normales"
        if not es_raro:
            canal_normales = bot.get_channel(CANAL_BIOMAS_NORMALES)
            if canal_normales:
                await canal_normales.send(
                    content="🟢 **Bioma Normal Detectado**",
                    embeds=message.embeds if message.embeds else None
                )

bot.run(TOKEN)
