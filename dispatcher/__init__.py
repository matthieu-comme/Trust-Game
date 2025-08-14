from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = "dispatcher"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    NUM_APPS = 3
    BASE_URL = "http://localhost:8000"
    USERNAME = "admin"
    PASSWORD = "admin"
    # insérer le code du session-wide link, et non le code de la session
    CODE_GROUPE_1 = "zanemofo"
    CODE_GROUPE_2 = "muzuvuge"
    CODE_GROUPE_3 = "pivijeno"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    group_number = models.IntegerField()


# FONCTIONS


def set_vars(player: Player):
    # répartit les joueurs 2 par 2 dans les groupes 1 à 3
    n = ((player.participant.id_in_session - 1) // 2) % 3 + 1
    player.group_number = n


def get_code(player: Player):
    n = player.group_number
    if n == 1:
        code = C.CODE_GROUPE_1
    elif n == 2:
        code = C.CODE_GROUPE_2
    else:
        code = C.CODE_GROUPE_3

    return code.strip()


class Welcome(Page):

    def vars_for_template(player: Player):
        pass

    def before_next_page(player: Player, timeout_happened):
        set_vars(player)


class Dispatch(Page):

    @staticmethod
    def vars_for_template(player: Player):
        code = get_code(player)
        return {
            "player_vars": player.participant.vars,
            "group_number": player.group_number,
            "code": code,
            "link": f'href="{C.BASE_URL}/join/{code}"',
        }


page_sequence = [Welcome, Dispatch]
