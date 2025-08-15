from otree.api import *
from openai import OpenAI
import random
import time
import os
from dotenv import load_dotenv

load_dotenv()

# récupère la clé openai
key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=key)


class C(BaseConstants):
    NAME_IN_URL = "tg"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = 10  # somme initiale du joueur A
    MULTIPLIER = 3
    CHAT_DURATION = 300  # Temps de conversation en secondes
    USER_PREFIX = "<strong>Joueur:</strong> "  # nom du joueur affiché avant son message dans le chat
    BOT_PREFIX = "<strong>GPT:</strong> "  # pareil pour gpt
    CHAT_SEPARATOR = "<br>"  # séparateur entre 2 messages
    NO_GPT_BEHAVIOR = "Non"
    # Modifier les deux paramètres suivants pour obtenir le traitement souhaité
    HAS_CHEAP_TALK = os.environ.get("HAS_CHEAP_TALK") == "True"
    GPT_BEHAVIOR = os.environ.get("GPT_BEHAVIOR")


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_sent = models.CurrencyField(min=0, max=C.ENDOWMENT)
    amount_sent_back = models.CurrencyField()
    talk_time = models.IntegerField()  # temps réel de conversation
    expire_time = models.FloatField()  # temps d'expiration du chat

    def set_payoffs(self):
        sent = self.amount_sent
        sent_back = self.amount_sent_back
        tripled = sent * C.MULTIPLIER

        p1: Player = self.get_player_by_id(1)
        p2: Player = self.get_player_by_id(2)

        p1.payoff = C.ENDOWMENT - sent + sent_back
        p2.payoff = tripled - sent_back


class Player(BasePlayer):
    p_role = models.StringField()
    partner_id = models.StringField()
    error_count = models.IntegerField(initial=0)  # nombre d'erreurs au quiz
    # Réponses des participants
    q1_b_receive = models.IntegerField(label="")
    q2_a_get_back = models.IntegerField(label="")
    q3_a_final = models.IntegerField(label="")
    q3_b_final = models.IntegerField(label="")
    q4_true_false = models.StringField(
        label="", choices=["Vrai", "Faux"], widget=widgets.RadioSelect
    )
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    message = models.LongStringField(blank=True)
    chat_history = models.LongStringField(initial="")
    gpt_history = models.LongStringField(initial="")

    gpt_behavior = models.StringField(initial=C.GPT_BEHAVIOR)
    has_cheap_talk = models.BooleanField(initial=C.HAS_CHEAP_TALK)


def set_partner_id(player: Player):
    partner = player.get_others_in_group()[0]
    uid = partner.participant.code
    id = str(partner.participant.id_in_session)
    player.partner_id = uid if uid else id


"""
# définis si le joueur a le cheap talk et / ou chatgpt, avec son attitude
# sur 8 duos ça fait par exemple : (has_cheap_talk, gpt_behavior)
# (False,Non), (False,Neutre), (False,Stratège), (False,Altruise), (True,Non), (True,Neutre), (True,Stratège), (True,Altruise)
def set_chat_options(player: Player):
    behaviors = C.BEHAVIORS
    nb_behaviors = len(behaviors)
    nb_participants = len(player.session.get_participants())
    id = player.participant.id_in_session
    index = ((id - 1) // 2) % nb_behaviors
    player.gpt_behavior = behaviors[index]

    # la deuxième moitié des joueurs a le cheap talk
    player.has_cheap_talk = id > nb_participants // 2
"""


class BaseQuiz(Page):
    form_model = "player"
    form_fields = [
        "q1_b_receive",
        "q2_a_get_back",
        "q3_a_final",
        "q3_b_final",
        "q4_true_false",
    ]

    @staticmethod
    def vars_for_template(player: Player):
        # affectation des éléments de questions
        player.x = random.randint(2, 10)

        mult = C.MULTIPLIER
        max_choice = mult * C.ENDOWMENT
        choice_list = [x for x in range(mult, max_choice + 1) if x % mult == 0]
        player.y = random.choice(choice_list)

        player.z = random.randint(1, player.y)
        return {
            "participant": player.participant,
            "x": player.x,
            "y": player.y,
            "z": player.z,
        }

    @staticmethod
    def error_message(player: Player, values):
        errors = {}
        correct_q1 = player.x * C.MULTIPLIER

        if values["q1_b_receive"] != correct_q1:
            player.error_count += 1
            errors["q1_b_receive"] = (
                f"Le joueur B reçoit {player.x} × {C.MULTIPLIER} = {correct_q1} jetons."
            )

        if values["q2_a_get_back"] != player.z:
            player.error_count += 1
            errors["q2_a_get_back"] = (
                f"Le joueur A reçoit ce que B renvoie : {player.z} jetons."
            )

        if values["q3_a_final"] != 8:
            player.error_count += 1
            errors["q3_a_final"] = "Revoir le calcul : 10 - 4 + 2 = 8 jetons."

        if values["q3_b_final"] != 10:
            player.error_count += 1
            errors["q3_b_final"] = "Revoir le calcul : 12 - 2 = 10 jetons."

        if values["q4_true_false"] != "Faux":
            player.error_count += 1
            errors["q4_true_false"] = (
                "C'est faux : les jetons renvoyés par B ne sont pas triplés."
            )

        return errors or None


class QuizExample1(BaseQuiz):
    pass


class Instructions(Page):

    def vars_for_template(player: Player):
        # set_chat_options(player)
        return {
            "gpt behavior": player.gpt_behavior,
            "has cheap talk": player.has_cheap_talk,
        }

    def before_next_page(player: Player, timeout_happened):
        player.p_role = "A" if player.id_in_group == 1 else "B"
        set_partner_id(player)


# gérer les messages du chat entre joueurs
def handle_chat_message(player: Player, data):
    if "message" in data:
        letter = "A" if player.id_in_group == 1 else "B"
        message_html = f"<strong>Joueur {letter}:</strong> {data['message']}<br>"
        responses = {}

        # update l'historique de tous les joueurs du groupe
        for p in player.group.get_players():
            p.chat_history += message_html
            responses[p.id_in_group] = {
                "new_message": message_html,
            }
        return responses
    else:
        return None


def chat_with_gpt(player: Player, data):
    user_message = data["message"]
    # historique sous forme de liste pour la requête
    messages_list = [  # c'est ici qu'on met les consignes pour chatgpt
        {"role": "system", "content": "Tu réponds en une à deux phrases simples."},
        {
            "role": "system",
            "content": f"Je joue au trust game. Donne moi des conseils pour favoriser un comportement {player.gpt_behavior}",
        },
    ]
    history = player.gpt_history or ""

    # reconstruit messages_list
    for line in history.strip().split(C.CHAT_SEPARATOR):
        if line.startswith(C.USER_PREFIX):  # message de user
            messages_list.append(
                {"role": "user", "content": line[len(C.USER_PREFIX) :]}
            )
        elif line.startswith(C.BOT_PREFIX):  # message de gpt
            messages_list.append(
                {"role": "assistant", "content": line[len(C.BOT_PREFIX) :]}
            )

    messages_list.append({"role": "user", "content": user_message})

    history += f"{C.USER_PREFIX}{user_message}<br>"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages_list,
    )
    bot_reply = response.choices[0].message.content

    history += f"{C.BOT_PREFIX}{bot_reply}<br>"
    player.gpt_history = history

    return {
        player.id_in_group: {
            "is_chat_gpt": True,
            "reply": bot_reply,
            "gpt_history": history,
            "bot_prefix": C.BOT_PREFIX,
        }
    }


def handle_typing_status(player: Player, data) -> dict:
    is_typing = data["typing_status"]
    responses = {}
    # Informer l'autre joueur uniquement
    for p in player.group.get_players():
        if p.id_in_group != player.id_in_group:
            responses[p.id_in_group] = {
                "other_player_typing": is_typing,
                "player_id": player.id_in_group,
            }
    return responses


def handle_amount_sent(player: Player, data) -> dict:
    amount = int(data["amount_sent"])
    group: Group = player.group
    if 0 <= amount <= C.ENDOWMENT:
        group.amount_sent = amount
        group.talk_time = int(C.CHAT_DURATION - (group.expire_time - time.time()))
        # Notifier les deux joueurs
        responses = {}
        for p in group.get_players():
            if p.id_in_group == 1:  # Joueur A
                responses[p.id_in_group] = {
                    "status": "sent",
                    "amount_sent": amount,
                }
            else:  # Joueur B
                responses[p.id_in_group] = {
                    "status": "received",
                    "amount_sent": amount,
                    "tripled_amount": int(amount * C.MULTIPLIER),
                }
        return responses


def handle_amount_sent_back(player: Player, data) -> dict:
    group: Group = player.group
    amount_back = int(data["amount_sent_back"])
    tripled_amount = int(group.amount_sent * C.MULTIPLIER)

    if 0 <= amount_back <= tripled_amount:
        group.amount_sent_back = amount_back
        # Notifier les deux joueurs que la transaction est complète
        responses = {}
        for p in group.get_players():
            responses[p.id_in_group] = {
                "status": "complete",
                "can_proceed": True,
                "amount_sent": group.amount_sent,
                "amount_sent_back": amount_back,
                "tripled_amount": tripled_amount,
            }
        group.set_payoffs()  # Calculer les gains
        return responses


class SyncWaitPage(WaitPage):

    def after_all_players_arrive(group: Group):
        if (
            group.field_maybe_none("expire_time") is None
        ):  # set le compte à rebours du chat
            group.expire_time = time.time() + C.CHAT_DURATION

    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        other_participant_number = other_player.participant.id_in_session
        return {
            "other_player": other_player,
            "other_participant_number": other_participant_number,
        }


class GamePlay(Page):

    def vars_for_template(player: Player):
        return {
            "has_chat_gpt": player.gpt_behavior != C.NO_GPT_BEHAVIOR,
            "gpt_behavior": player.gpt_behavior,
            "gpt_history": player.gpt_history,
            "chat_history": player.chat_history,
        }

    @staticmethod
    def live_method(player: Player, data):
        if "is_chat_gpt" in data:
            return chat_with_gpt(player, data)

        # cheap talk
        if "message" in data:
            return handle_chat_message(player, data)

        # indicateur de frappe
        if "typing_status" in data:
            return handle_typing_status(player, data)

        # envoi de jetons par le joueur A
        if "amount_sent" in data and player.id_in_group == 1:
            return handle_amount_sent(player, data)

        # renvoi de jetons par le joueur B
        if "amount_sent_back" in data and player.id_in_group == 2:
            return handle_amount_sent_back(player, data)

        return None

    @staticmethod
    def js_vars(player: Player):
        group: Group = player.group
        return {
            "id_in_group": player.id_in_group,
            "endowment": C.ENDOWMENT,
            "multiplier": C.MULTIPLIER,
            "amount_sent": group.field_maybe_none("amount_sent"),
            "amount_sent_back": group.field_maybe_none("amount_sent_back"),
        }


class WaitForResults(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs()


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group: Group = player.group
        sent = int(group.amount_sent)
        sent_back = int(group.amount_sent_back)
        tripled = sent * C.MULTIPLIER
        return dict(
            sent=sent,
            sent_back=sent_back,
            tripled=tripled,
            payoff=int(player.payoff),
            is_test_round=(player.round_number == 1),
        )


page_sequence = [
    #Instructions,
    #QuizExample1,
    SyncWaitPage,
    GamePlay,
    Results,
]
