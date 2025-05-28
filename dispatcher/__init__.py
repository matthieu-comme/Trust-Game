from otree.api import *
import itertools


class C(BaseConstants):
    NAME_IN_URL = "dispatcher"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    PERMUTATIONS = list(
        itertools.permutations(["questionnaire", "trust_game", "risk_aversion"])
    )


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


class Welcome(Page):
    """Page de bienvenue avant le dispatcher"""

    @staticmethod
    def vars_for_template(player):
        return dict()


class Dispatch(Page):
    @staticmethod
    def before_next_page(player, timeout_happened):
        if "app_order" not in player.participant.vars:
            group_size = 20
            perm_index = (player.participant.id_in_session - 1) // group_size
            app_order = list(C.PERMUTATIONS[perm_index % len(C.PERMUTATIONS)])
            player.participant.vars["app_order"] = app_order
            player.participant.vars["app_index"] = 0

    @staticmethod
    def vars_for_template(player):
        if "app_order" not in player.participant.vars:
            group_size = 20
            perm_index = (player.participant.id_in_session - 1) // group_size
            app_order = list(C.PERMUTATIONS[perm_index % len(C.PERMUTATIONS)])
            player.participant.vars["app_order"] = app_order
            player.participant.vars["app_index"] = 0

        return dict(
            app_order=player.participant.vars["app_order"],
            group_number=(player.participant.id_in_session - 1) // 20 + 1,
        )

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        index = player.participant.vars["app_index"]
        app_to_go = player.participant.vars["app_order"][index]
        player.participant.vars["app_index"] += 1
        return app_to_go


page_sequence = [Welcome, Dispatch]
