import os
import threading
from flask import Flask
import discord
from discord.ext import commands

# -------------------------------------------------------------
# 1. SERVIDOR WEB CON FLASK (Para evitar errores de puerto en Render)
# -------------------------------------------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot activo 24/7 en Render"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Inicia el servidor Flask en un hilo secundario
threading.Thread(target=run_flask, daemon=True).start()

# -------------------------------------------------------------
# 2. CONFIGURACIÓN DEL BOT DE DISCORD
# -------------------------------------------------------------
TOKEN = os.getenv('BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ID del canal donde la macro de Roblox publica las alertas
CANAL_LOGS_UNICO = 1549939549151563858  

# IDs de los canales para BIOMAS RAROS
BIOMES_RAROS = {
    "dreamspace": 1549937750638075995,   # #dreamspace
    "glitched":   1549943866109595708,   # #glitched
    "cyberspace": 1549943902675542137,   # #cyberspace
    "singularity": 1549943953892311140   # #singularity
}

# ID del canal para BIOMAS NORMALES
CANAL_BIOMAS_NORMALES = 1549943997630513333  # #biomas-normales

# -------------------------------------------------------------
# 3. EVENTOS DEL BOT
# -------------------------------------------------------------
@bot.event
async def on_ready():
    print(f"Bot conectado exitosamente como {bot.user}")

@bot.event
async def on_message(message):
    # Ignorar mensajes enviados por el propio bot
    if message.author == bot.user:
        return

    # Verificar si el mensaje viene del canal de logs original
    if message.channel.id == CANAL_LOGS_UNICO:
        contenido_buscar = ""
        
        # Buscar texto en el cuerpo del mensaje
        if message.content:
            contenido_buscar += message.content.lower() + " "
        
        # Buscar texto dentro de los embeds (recuadros con fotos/detalles)
        for embed in message.embeds:
            if embed.title:
                contenido_buscar += embed.title.lower() + " "
            if embed.description:
                contenido_buscar += embed.description.lower() + " "
            for field in embed.fields:
                contenido_buscar += field.name.lower() + " " + field.value.lower() + " "

        # Por defecto asigna el canal de biomas normales
        canal_destino_id = CANAL_BIOMAS_NORMALES 

        # Revisar si se detecta alguno de los biomas raros
        for bioma, canal_id in BIOMES_RAROS.items():
            if bioma in contenido_buscar:
                canal_destino_id = canal_id
                break

        # Obtener el canal de destino
        canal_destino = bot.get_channel(canal_destino_id)
        if canal_destino:
            # Reenviar el texto si existe
            if message.content:
                await canal_destino.send(message.content)
            
            # Reenviar los embeds (recuadros/imágenes) si existen
            for embed in message.embeds:
                await canal_destino.send(embed=embed)

    await bot.process_commands(message)

# -------------------------------------------------------------
# 4. INICIAR EL BOT
# -------------------------------------------------------------
if __name__ == "__main__":
    bot.run(TOKEN)
