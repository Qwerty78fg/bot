import asyncio
from flask import Flask, render_template, jsonify
import discord

app = Flask(__name__)

intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)

data_ready_event = asyncio.Event()

members_data = []
roles_data = []

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    global members_data, roles_data
    members_data = [{"name": member.name, "id": member.id} for member in bot.guilds[0].members]
    roles_data = [{"name": role.name, "id": role.id} for role in bot.guilds[0].roles]
    
    data_ready_event.set()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/members')
def get_members():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(data_ready_event.wait())
        return jsonify(members_data)
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/roles')
def get_roles():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(data_ready_event.wait())
        return jsonify(roles_data)
    except Exception as e:
        return jsonify({"error": str(e)})

def run_flask():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    with open("token.txt", "r") as f:
        token = f.read().strip()

    from threading import Thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    
    bot.run(token)
