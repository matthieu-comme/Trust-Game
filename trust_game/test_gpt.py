import openai
import json

"""
Nécessite de créer un fichier 'config.json' avec ceci dedans:
{
    "OPENAI_API_KEY": "INSERER_LA_CLE_ICI"
}
"""
with open("config.json") as f:
    config = json.load(f)

key = config["OPENAI_API_KEY"]

client = openai.OpenAI(api_key=key)

# historique des messages, avec consigne initiale
messages = [
    {
        "role": "system",
        "content": "Tu vas répondre en maximum 2 phrases.",
    },
    {
        "role": "system",
        "content": "Tu vas répondre en mix de français et d'anglais.",
    },
    {
        "role": "system",
        "content": "Tu vas conclure chaque réponse par des points de suspension",
    },
]
print("La discussion commence, écrivez 'STOP' pour l'arrêter")

while True:
    user_msg = input("\nVous: ")
    if str.lower(user_msg) == ("stop"):
        break
    # ajout de la demande à l'historique
    messages.append({"role": "user", "content": user_msg})

    reply = client.responses.create(
        model="gpt-3.5-turbo",
        input=messages,
    ).output_text

    # ajout de la réponse

    messages.append({"role": "assistant", "content": reply})

    print(f"GPT: {reply}")
