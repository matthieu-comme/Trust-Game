from otree.api import *
from openai import OpenAI
import json

# récupère la clé openai
with open("config.json") as f:
    config = json.load(f)

key = config["OPENAI_API_KEY"]
client = OpenAI(api_key=key)


class C(BaseConstants):
    NAME_IN_URL = "chatgpt"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    USER_PREFIX = "Joueur: "  # nom du joueur affiché avant son message dans le chat
    BOT_PREFIX = "GPT: "  # pareil pour gpt


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    chat_history = models.LongStringField(initial="")  # texte concaténé


def chat_with_gpt(player: Player, data):
    user_message = data["message"]
    # historique sous forme de liste pour la requête
    messages_list = [
        {"role": "system", "content": "Tu réponds en une à deux phrases simples."}
    ]
    history = player.chat_history or ""

    # reconstruit messages_list
    for line in history.strip().split("\n"):
        if line.startswith(C.USER_PREFIX):  # message de user
            messages_list.append(
                {"role": "user", "content": line[len(C.USER_PREFIX) :]}
            )
        elif line.startswith(C.BOT_PREFIX):  # message de gpt
            messages_list.append(
                {"role": "assistant", "content": line[len(C.BOT_PREFIX) :]}
            )

    messages_list.append({"role": "user", "content": user_message})

    history += f"\n{C.USER_PREFIX}{user_message}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_list,
    )
    bot_reply = response.choices[0].message.content

    history += f"\n{C.BOT_PREFIX}{bot_reply}"
    player.chat_history = history

    return {player.id_in_group: {"reply": bot_reply, "chat_history": history}}


# PAGES
class ChatPage(Page):

    live_method = "chat_with_gpt"

    def vars_for_template(player: Player):
        return {"chat_history": player.chat_history}


page_sequence = [ChatPage]
