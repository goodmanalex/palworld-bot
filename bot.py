import discord
from discord.ext import commands
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Cargar registros desde el archivo JSON (si existe)
def cargar_registros():
    try:
        with open("registros.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Guardar registros en el archivo JSON
def guardar_registros():
    with open("registros.json", "w") as f:
        json.dump(registro, f, indent=4)

# Base de datos en memoria (cargada desde el archivo)
registro = cargar_registros()

@bot.command()
async def registrar(ctx, *, nombre_juego):
    usuario = ctx.author

    if usuario.id in registro:
        await ctx.send(f"{usuario.mention}, ya estás registrado con el nombre **{registro[usuario.id]['juego']}**.\n"
                       "Si quieres modificar tu nombre, usa el comando `!editar <nuevo_nombre>`.")
        return

    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro[usuario.id] = {
        "discord": usuario.name,
        "juego": nombre_juego,
        "fecha_registro": fecha_registro
    }
    guardar_registros()

    await ctx.send(f"{usuario.mention}, tu nombre en Palworld ha sido registrado como **{nombre_juego}**.\n"
                   "Para ver la lista de usuarios registrados, usa el comando `!lista`.")

@bot.command()
async def editar(ctx, *, nuevo_nombre):
    usuario = ctx.author
    if usuario.id in registro:
        registro[usuario.id]["juego"] = nuevo_nombre
        guardar_registros()

        await ctx.send(f"{usuario.mention}, tu nombre ha sido actualizado a **{nuevo_nombre}**.\n"
                       "Para ver la lista de usuarios registrados, usa el comando `!lista`.")
    else:
        await ctx.send("No tienes ningún nombre registrado. Usa `!registrar <nombre>` primero.")

@bot.command()
async def lista(ctx):
    if not registro:
        await ctx.send("No hay registros aún.")
        return

    usuarios_ordenados = sorted(registro.values(), key=lambda x: x['discord'])
    mensaje = "**Lista de nombres registrados:**\n"
    for r in usuarios_ordenados:
        mensaje += f"- **{r['discord']}** = {r['juego']} (Registrado el {r['fecha_registro']})\n"

    await ctx.send(mensaje)

@bot.event
async def on_ready():
    print(f"✅ El bot está conectado como {bot.user}")

bot.run("MTM1OTU2NDc3ODE5MTg1MTgzMQ.Gyur7o.UQXQdiE5iUSg2el3d7RdWuUxXKi4wyBFj_Kzdc")  # ← Vamos a reemplazar esto en el siguiente paso