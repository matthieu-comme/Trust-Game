from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "results"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Intro(Page):
    pass


class Results(Page):
    def vars_for_template(player: Player):
        vars = player.participant.vars
        print(vars)
        return {
            "chosen_decision": vars["chosen_decision"],
            "invested": vars["invested"],
            "ball_color": vars["ball_color"],
            'initial_amount': vars['initial_amount'],
            "profit": vars["profit"],
            "payoff": vars["payoff"],
        }


page_sequence = [Intro, Results]
