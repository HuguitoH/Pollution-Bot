import discord
import random

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

commands = {
    '/hello': 'Saludar',
    '/pollution': 'Definición de Contaminación',
    '/tips': 'Consejos sobre cómo reducir la contaminación',
    '/recycle': 'Informa sobre cómo reciclar diferentes tipos de materiales',
    '/daily': 'Obtener un consejo aleatorio diario',
    '/suggest': 'Sugerir temas o preguntas para futuras actualizaciones del bot',
    '/suggestions': 'Ver las sugerencias registradas',
    '/clear': 'Limpiar el chat del canal actual'  # Agregar el nuevo comando
}

daily_tips = [
    "Apaga las luces cuando no las necesites para ahorrar energía.",
    "Usa una botella de agua reutilizable en lugar de botellas de plástico.",
    "Recuerda separar tus residuos correctamente para facilitar el reciclaje.",
    "Dúchate en lugar de bañarte para ahorrar agua.",
    "Compra productos locales y de temporada para reducir la huella de carbono.",
    "Utiliza el transporte público o comparte viajes en automóvil para reducir la contaminación.",
    "Apaga tus dispositivos electrónicos por la noche para ahorrar energía.",
    "Reutiliza bolsas de compras y envases siempre que sea posible.",
    "Planta árboles y flores en tu comunidad para mejorar la calidad del aire.",
    "Consume menos carne y lácteos para reducir el impacto ambiental de tu dieta."
]

used_tips = []
suggestions = []

@client.event
async def on_ready():
    print(f'Iniciamos sesión como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/hello'):
        await message.channel.send(f'¡Hola, soy {client.user}! ¡Encantado de conocerte, cómo puedo ayudarte?')
    elif message.content.startswith('/pollution'):
        await pollution(message.channel)
    elif message.content.startswith('/tips'):
        await send_tips(message.channel)
    elif message.content.startswith('/recycle'):
        await recycle(message.channel)
    elif message.content.startswith('/daily'):
        await daily_tip(message.channel)
    elif message.content.startswith('/suggest'):
        suggestion = message.content[len('/suggest'):].strip()
        if suggestion:
            suggestions.append(suggestion)
            print("Sugerencia registrada:", suggestion)  
            await message.channel.send("¡Gracias por tu sugerencia! La hemos registrado para futuras actualizaciones.")
    elif message.content.startswith('/suggestions'):  
        await send_suggestions(message.channel)
    elif message.content.startswith('/clear'):  # Agregar manejo para el comando '/clear'
        await clear_messages(message.channel)
    elif message.content.startswith('/help'):
        await send_help(message.channel)
    else:
        await message.channel.send("¡No puedo procesar este comando, lo siento!")

async def send_help(channel):
    help_message = "Comandos disponibles:\n"
    for command, description in commands.items():
        help_message += f"{command}: {description}\n"
    await channel.send(help_message)

async def send_tips(channel):
    tips_message = "Consejos sobre cómo reducir la contaminación:\n"
    for tip in daily_tips:
        tips_message += f"{tip}\n"
    await channel.send(tips_message)

async def pollution(channel):
    pollution_definition = "La contaminación es la introducción de contaminantes en el medio ambiente natural que causa un cambio adverso."
    await channel.send(pollution_definition)

async def recycle(channel):
    recycle_info = (
        "**Contenedores de reciclaje y sus materiales correspondientes:**\n\n"
        "🔵 **Contenedor Azul (Papel y Cartón)**: Periódicos, revistas, papel de oficina, cartón, cajas de cartón, etc.\n\n"
        "🟡 **Contenedor Amarillo (Envases de Plástico, Latas y Tetra Brik)**: Botellas de plástico, envases de plástico, latas de aluminio, latas de conserva, envases de Tetra Brik, etc.\n\n"
        "🟢 **Contenedor Verde (Vidrio)**: Botellas de vidrio, frascos de vidrio, tarros de conserva, etc.\n\n"
        "⚪ **Contenedor Blanco (Pilas y Baterías)**: Pilas alcalinas, pilas recargables, baterías de móviles, etc.\n\n"
        "⚫ **Contenedor Negro (Resto o Residuos no Reciclables)**: Residuos que no son reciclables como pañales, colillas de cigarrillos, etc.\n"
    )
    await channel.send(recycle_info)

async def daily_tip(channel):
    if len(used_tips) == len(daily_tips):
        await channel.send("¡Ya has recibido todos los consejos! ¡Vuelve mañana para uno nuevo!")
        return
    
    tip = random.choice([t for t in daily_tips if t not in used_tips])
    used_tips.append(tip)
    
    await channel.send(f"Aquí tienes tu consejo diario: {tip}")

async def send_suggestions(channel):
    if suggestions:
        await channel.send("Aquí están las sugerencias que hemos recibido hasta el momento:")
        for index, suggestion in enumerate(suggestions, start=1):
            await channel.send(f"{index}. {suggestion}")
    else:
        await channel.send("No hemos recibido ninguna sugerencia hasta el momento.")

async def clear_messages(channel):
    await channel.purge(limit=100)  # Elimina hasta 100 mensajes del canal

client.run('token')
