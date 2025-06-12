from otree.api import *
import random
import time


class C(BaseConstants):
    NAME_IN_URL = "trust_game"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = 10  # somme initiale du joueur A
    MULTIPLIER = 3
    CHAT_DURATION = 120  # 2 min de conversation


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_sent = models.CurrencyField(min=0, max=C.ENDOWMENT)
    amount_sent_back = models.CurrencyField()
    expire_time = models.FloatField()  # temps d'expiration du chat

    def set_payoffs(self):
        sent = self.amount_sent
        sent_back = self.amount_sent_back
        tripled = sent * C.MULTIPLIER

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)

        p1.payoff = C.ENDOWMENT - sent + sent_back
        p2.payoff = tripled - sent_back


class Player(BasePlayer):
    # Réponses des participants
    q1_b_receive = models.IntegerField()
    q2_a_get_back = models.IntegerField()
    q3_a_final = models.IntegerField()
    q3_b_final = models.IntegerField()
    q4_true_false = models.StringField(
        label="", choices=["Vrai", "Faux"], widget=widgets.RadioSelect
    )
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    message = models.LongStringField(blank=True)
    chat_history = models.LongStringField(initial="")


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
            errors["q1_b_receive"] = (
                f"Le joueur B reçoit {player.x} × {C.MULTIPLIER} = {correct_q1} jetons."
            )

        if values["q2_a_get_back"] != player.z:
            errors["q2_a_get_back"] = (
                f"Le joueur A reçoit ce que B renvoie : {player.z} jetons."
            )

        if values["q3_a_final"] != 8:
            errors["q3_a_final"] = "Revoir le calcul : 10 - 4 + 2 = 8 jetons."
        if values["q3_b_final"] != 10:
            errors["q3_b_final"] = "Revoir le calcul : 12 - 2 = 10 jetons."

        if values["q4_true_false"] != "Faux":
            errors["q4_true_false"] = (
                "C'est faux : les jetons renvoyés par B ne sont pas triplés."
            )

        return errors or None


class QuizExample1(BaseQuiz):
    pass


class Instructions(Page):
    pass


# Méthode commune pour gérer les messages du chat
def handle_chat_message(player: Player, data):
    if "message" in data:
        letter = "A" if player.id_in_group == 1 else "B"
        message_html = f"<strong>Joueur {letter}:</strong> {data['message']}<br>"

        # Ajouter le message à l'historique du chat du joueur
        player.chat_history += message_html

        # Préparer les réponses pour tous les joueurs
        responses = {}

        # Mettre à jour l'historique de tous les joueurs du groupe
        for p in player.group.get_players():
            if p.id_in_group != player.id_in_group:
                p.chat_history += message_html
                responses[p.id_in_group] = {
                    "new_message": message_html,
                    "full_chat": p.chat_history,
                }
            else:
                responses[p.id_in_group] = {"full_chat": p.chat_history}

        return responses
    return None


class SyncWaitPage(WaitPage):

    def after_all_players_arrive(group: Group):
        if group.field_maybe_none("expire_time") is None:
            group.expire_time = time.time() + C.CHAT_DURATION

    def vars_for_template(player: Player):
        other_player = player.get_others_in_group()[0]
        other_participant_number = other_player.participant.id_in_session
        return {
            "other_player": other_player,
            "other_participant_number": other_participant_number,
        }


class GamePlay(Page):

    @staticmethod
    def live_method(player: Player, data):

        if "time_remaining" in data:
            player.time_remaining = data["time_remaining"]
        # Gérer les messages du chat
        if "message" in data:
            return handle_chat_message(player, data)

        # Gérer l'indicateur de frappe
        if "typing_status" in data:
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

        # Gérer l'envoi de jetons par le joueur A
        if "amount_sent" in data and player.id_in_group == 1:
            amount = float(data["amount_sent"])
            if 0 <= amount <= C.ENDOWMENT:
                player.group.amount_sent = amount
                # Notifier les deux joueurs
                responses = {}
                for p in player.group.get_players():
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

        # Gérer le renvoi de jetons par le joueur B
        if "amount_sent_back" in data and player.id_in_group == 2:
            amount_back = float(data["amount_sent_back"])
            tripled_amount = int(player.group.amount_sent * C.MULTIPLIER)

            if 0 <= amount_back <= tripled_amount:
                player.group.amount_sent_back = amount_back
                # Notifier les deux joueurs que la transaction est complète
                responses = {}
                for p in player.group.get_players():
                    responses[p.id_in_group] = {
                        "status": "complete",
                        "can_proceed": True,
                        "amount_sent": player.group.amount_sent,
                        "amount_sent_back": amount_back,
                        "tripled_amount": tripled_amount,
                    }
                player.group.set_payoffs()  # Calculer les gains
                return responses

        return None

    @staticmethod
    def js_vars(player: Player):
        return {
            "id_in_group": player.id_in_group,
            "endowment": C.ENDOWMENT,
            "multiplier": C.MULTIPLIER,
        }


class WaitForResults(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.set_payoffs()


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
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
    Instructions,
    # QuizExample1,
    SyncWaitPage,
    GamePlay,
    Results,
]
