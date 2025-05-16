from flask import Flask, render_template, request, jsonify
import requests
import json
import os

app = Flask(__name__)

with open("strategies.json") as f:
    strategies = json.load(f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json["message"]
    response = process_query(user_input)
    return jsonify(response)

def process_query(query):
    query = query.lower().strip()

    if "info" in query or "tell me about" in query:
        name = query.split()[-1]
        return get_pokemon_info(name)

    elif "strategy" in query or "how to use" in query:
        name = query.split()[-1].capitalize()
        strategy = strategies.get(name)
        if strategy:
            return {"text": f"⚔️ Strategy for {name}:<br>{strategy}", "image": None}
        else:
            return {"text": f"No strategy found for {name}.", "image": None}

    return {"text": "❓ I didn't understand. Try 'Tell me about Pikachu' or 'Strategy for Charizard'.", "image": None}

def get_pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name.lower()}"
    res = requests.get(url)

    if res.status_code != 200:
        return {"text": "❌ Pokémon not found. Please check the name.", "image": None}

    data = res.json()

    types = ", ".join([t["type"]["name"].capitalize() for t in data["types"]])
    abilities = ", ".join([a["ability"]["name"].capitalize() for a in data["abilities"]])
    stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
    sprite_url = data["sprites"]["front_default"]
    stats_display = "<br>".join([f"{k.capitalize()}: {v}" for k, v in stats.items()])

    return {
        "text": f"""
        🧬 <strong>Name:</strong> {name.capitalize()}<br>
        🔥 <strong>Type:</strong> {types}<br>
        💡 <strong>Abilities:</strong> {abilities}<br>
        📊 <strong>Base Stats:</strong><br>{stats_display}
        """,
        "image": sprite_url
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)