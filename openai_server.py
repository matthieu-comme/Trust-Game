from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS
from dotenv import load_dotenv
import json

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")
with open("config.json") as f:
    config = json.load(f)

key = config["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=key)

app = Flask(__name__)
CORS(app)  # pour accepter les appels depuis oTree (navigateur)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    reply = client.responses.create(
        model="gpt-3.5-turbo",
        input=messages,
    ).output_text

    return jsonify({"reply": reply})


@app.route("/", methods=["GET"])
def index():
    return "Flask GPT backend is running."


if __name__ == "__main__":
    app.run(port=5000)
