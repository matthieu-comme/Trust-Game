from otree.api import *
import random

doc = """
Tâche de mesure de l'aversion au risque et de l'aversion à l'ambiguïté dans les gains et les pertes
avec une tâche préliminaire (comptage de chiffres dans π).
"""


class C(BaseConstants):
    NAME_IN_URL = "risk_aversion"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(30)
    MAX_INVESTMENT = 10
    PI_DIGITS = (
        "141 592 653 589 793 238 462 643 383 279 502 884 197 169 399 375 10"
        "5 820 974 944 592 307 816 406 286 208 998 628 034 825 342 117 067 9"
        "82 148 086 513 282 306 647 093 844 609 550 582 231 725 359 408 128"
        "48 111 745 028 410 270 193 852 110 555 964 462 294 895 493 038 196"
    )



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Tâche de comptage
    target_digit = models.IntegerField(initial=0)  # Added initial value to avoid None
    pi_count = models.IntegerField(label="Combien de fois ce chiffre apparaît-il ?")
    task_success = models.BooleanField(initial=False)

    inv1 = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)], initial=0, label="Je décide d'investir :")
    inv2 = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)], label="Je décide d'investir :")
    inv3 = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)], label="Je décide d'investir :")
    inv4 = models.IntegerField(choices=[(i, str(i)) for i in range(0, 11)], label="Je décide d'investir :")

class CountDigitTask(Page):
    form_model = "player"
    form_fields = ["pi_count"]

    @staticmethod
    def error_message(player, values):
        correct_count = C.PI_DIGITS.count(str(player.target_digit))
        if values["pi_count"] != correct_count:
            return f"Incorrect. Réessayez."
        else:
            player.task_success = True

    def vars_for_template(player):
        return dict(
            pi_digits=C.PI_DIGITS,
            digit=player.target_digit,
        )

    def before_next_page(player, timeout_happened):
        player.payoff = C.ENDOWMENT

    #def is_displayed(player):
    #    return not player.task_success

class GeneralInfo(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Assign a random digit when moving from Instructions to CountDigitTask
        player.target_digit = random.randint(0, 9)

    def vars_for_template(player):
        return {
            "etape": "la mesure d'aversion au risque et à l'ambiguité",             
        }

class InvestmentIntroduction(Page):
    def is_displayed(player):
        return player.task_success


class InvestmentIntro1(Page):
    pass

class InvestmentDecision1(Page):
    form_model = "player"
    form_fields = ["inv1"]


class InvestmentConfirm1(Page):
    def vars_for_template(player: Player):
        return {'payoff': player.payoff}
        # DÉCISION 2

class InvestmentIntro2(Page):
    pass

class InvestmentDecision2(Page):
    form_model = "player"
    form_fields = ["inv2"]


def vars_for_template(player):
    if player.inv2 is not None:
        invested = player.inv2
    else:
        invested = 0  # valeur par défaut

    kept = 10 - invested
    return {
        "invested": invested,
        "kept": kept,
        "gain_if_yellow": kept + 3 * invested,
        "gain_if_purple": kept,
    }


class InvestmentConfirm2(Page):
    def vars_for_template(player):
        return {
            "invested": player.inv2,
            "kept": 10 - player.inv2,
            "gain_if_yellow": (10 - player.inv2) + 3 * player.inv2,
            "gain_if_purple": 10 - player.inv2,
        }


# DÉCISION 3

class InvestmentIntro3(Page):
    pass

class InvestmentDecision3(Page):
    form_model = "player"
    form_fields = ["inv3"]


class InvestmentConfirm3(Page):
    def vars_for_template(player):
        non_invested = 10 - player.inv3
        return {
            "invested": player.inv3,
            "non_invested": non_invested,
            "total_loss_yellow": non_invested,
            "total_loss_purple": non_invested + 3 * player.inv3,
        }


# DÉCISION 4

class InvestmentIntro4(Page):
    pass

class InvestmentDecision4(Page):
    form_model = "player"
    form_fields = ["inv4"]


class InvestmentConfirm4(Page):
    def vars_for_template(player):
        non_invested = 10 - player.inv4
        return {
            "invested": player.inv4,
            "non_invested": non_invested,
            "total_loss_yellow": non_invested,
            "total_loss_purple": non_invested + 3 * player.inv4,
        }

page_sequence = [
    #GeneralInfo,
    CountDigitTask,
    InvestmentIntroduction,
    InvestmentIntro1,
    InvestmentDecision1,
    InvestmentConfirm1,
    InvestmentIntro2,
    InvestmentDecision2,
    InvestmentConfirm2,
    InvestmentIntro3,
    InvestmentDecision3,
    InvestmentConfirm3,
    InvestmentIntro4,
    InvestmentDecision4,
    InvestmentConfirm4,
]
