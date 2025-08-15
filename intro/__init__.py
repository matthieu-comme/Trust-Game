from otree.api import *
from datetime import datetime

doc = """
Module permettant de définir certaines variables avant de le début de l'expérience
"""


class C(BaseConstants):
    NAME_IN_URL = "intro"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ORDRES_ETAPES = ["Ordre not found", "Q/A/TG", "A/Q/TG", "Q/TG/A"]
    SHOW_UP_FEE = 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    date = models.StringField()
    ordre_etapes = models.StringField()


def set_vars(player: Player):
    config_name = player.session.config["name"]
    if config_name == "groupe_1":
        n = 1
    elif config_name == "groupe_2":
        n = 2
    elif config_name == "groupe_3":
        n = 3
    else:
        n = 0
    player.ordre_etapes = C.ORDRES_ETAPES[n]

    date = datetime.now().strftime("%d-%b-%y")
    player.date = date

    player.participant.vars["show_up_fee"] = C.SHOW_UP_FEE


# PAGES
class MyPage(Page):
    def before_next_page(player: Player, timeout_happened):
        set_vars(player)


page_sequence = [MyPage]
