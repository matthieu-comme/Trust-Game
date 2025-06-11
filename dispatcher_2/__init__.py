from otree.api import *
import requests
from bs4 import BeautifulSoup


class C(BaseConstants):
    NAME_IN_URL = "dispatcher_2"
    PLAYERS_PER_GROUP = 60
    NUM_ROUNDS = 1
    NUM_APPS = 3
    BASE_URL = "http://localhost:8000"
    USERNAME = "admin"
    PASSWORD = "admin"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # attribution des permutations
    def set_app_order(self):
        if "app_order" not in self.participant.vars:
            perm_index = (self.participant.id_in_session - 1) // C.PLAYERS_PER_GROUP
            app_order = list(C.PERMUTATIONS[perm_index % len(C.PERMUTATIONS)])
            self.participant.vars["app_order"] = app_order
            self.participant.vars["app_index"] = 0


# FONCTIONS


def get_all_link_codes(session_code: str) -> list:
    s = requests.Session()

    # si connexion à otree nécessaire
    # s.post(f'{C.BASE_URL}/accounts/login/', data={'username': C.USERNAME,'password': C.PASSWORD,})
    r = s.get(f"{C.BASE_URL}/SessionStartLinks/{session_code}")

    soup = BeautifulSoup(r.text, "html.parser")

    result = []
    for a in soup.select(".participant-link"):
        link_code = a.getText().split("/")[-1]
        result.append(link_code)

    return result


class Welcome(Page):
    """Page de bienvenue avant le dispatcher"""

    def vars_for_template(player: Player):
        return {"perm": C.PERMUTATIONS}

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.set_app_order()


class Dispatch(Page):

    @staticmethod
    def vars_for_template(player: Player):
        # player.set_app_order()

        return {
            "participant.vars": player.participant.vars,
            "app_order": player.participant.vars["app_order"],
            "group_number": (player.participant.id_in_session - 1) // 20 + 1,
        }

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        index = player.participant.vars["app_index"]
        if index < 3:
            app_to_go = player.participant.vars["app_order"][index]
            player.participant.vars["app_index"] += 1
            return app_to_go


page_sequence = [Welcome, Dispatch]
