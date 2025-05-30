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
    target_digit = models.IntegerField(initial=0)
    pi_count = models.IntegerField(label="Combien de fois ce chiffre apparaît-il ?")

    i_decision = models.IntegerField(initial=1)

    inv1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, 11)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv2 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, 11)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv3 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, 11)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv4 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, 11)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv5 = models.StringField(
        choices=["A", "B", "C", "D"], label="Je choisis le tirage :"
    )
    inv6 = models.StringField(
        choices=["A", "B", "C", "D"], label="Je choisis le tirage :"
    )
    inv7 = models.StringField(
        choices=["A", "B", "C", "D"], label="Je choisis le tirage :"
    )
    inv8 = models.StringField(
        choices=["A", "B", "C", "D"], label="Je choisis le tirage :"
    )


class CountDigitTask(Page):
    form_model = "player"
    form_fields = ["pi_count"]

    @staticmethod
    def error_message(player, values):
        correct_count = C.PI_DIGITS.count(str(player.target_digit))
        if values["pi_count"] != correct_count:
            return f"Incorrect. Réessayez."

    def vars_for_template(player):
        return dict(
            pi_digits=C.PI_DIGITS,
            digit=player.target_digit,
        )

    def before_next_page(player, timeout_happened):
        player.payoff = C.ENDOWMENT


class GeneralInfo(Page):

    @staticmethod
    def before_next_page(player, timeout_happened):
        pass
        # player.target_digit = random.randint(0, 9)

    def vars_for_template(player):
        return {
            "etape": "la mesure d'aversion au risque et à l'ambiguité",
        }


class TaskSuccess(Page):
    pass


class InvestmentConfirm(Page):

    def is_displayed(player: Player):
        i = player.i_decision
        result = (
            i <= 4
            or (i == 5 and player.inv1 == 10)
            or (i == 6 and player.inv2 == 10)
            or (i == 7 and player.inv3 == 10)
            or (i == 8 and player.inv4 == 10)
            or (i == 9)
        )
        if not result:
            player.i_decision += 1
        return result

    def before_next_page(player: Player, timeout_happened):
        player.i_decision += 1

    def vars_for_template(player: Player):
        return {
            "i_decision": player.i_decision,
            "inv1_4": [player.inv1, player.inv2, player.inv3, player.inv4],
            "inv5_8": [
                player.field_maybe_none("inv5"),
                player.field_maybe_none("inv6"),
                player.field_maybe_none("inv7"),
                player.field_maybe_none("inv8"),
            ],
        }


class InvestmentIntro1(Page):
    pass


class InvestmentDecision1(Page):
    form_model = "player"
    form_fields = ["inv1"]


class InvestmentIntro2(Page):
    pass


class InvestmentDecision2(Page):
    form_model = "player"
    form_fields = ["inv2"]


class InvestmentIntro3(Page):
    pass


class InvestmentDecision3(Page):
    form_model = "player"
    form_fields = ["inv3"]


class InvestmentIntro4(Page):
    pass


class InvestmentDecision4(Page):
    form_model = "player"
    form_fields = ["inv4"]


class InvestmentDecision5(Page):
    form_model = "player"
    form_fields = ["inv5"]

    def is_displayed(player: Player):
        return player.inv1 == 10

    def vars_for_template(player: Player):
        return {
            "i_decision": player.i_decision,
            "inv1_4": [player.inv1, player.inv2, player.inv3, player.inv4],
            "inv5_8": [
                player.field_maybe_none("inv5"),
                player.field_maybe_none("inv6"),
                player.field_maybe_none("inv7"),
                player.field_maybe_none("inv8"),
            ],
        }


class InvestmentDecision6(Page):
    form_model = "player"
    form_fields = ["inv6"]

    def is_displayed(player: Player):
        return player.inv2 == 10

    def vars_for_template(player: Player):
        return {
            "i_decision": player.i_decision,
            "inv1_4": [player.inv1, player.inv2, player.inv3, player.inv4],
            "inv5_8": [
                player.field_maybe_none("inv5"),
                player.field_maybe_none("inv6"),
                player.field_maybe_none("inv7"),
                player.field_maybe_none("inv8"),
            ],
        }


class InvestmentDecision7(Page):
    form_model = "player"
    form_fields = ["inv7"]

    def is_displayed(player: Player):
        return player.inv3 == 10

    def vars_for_template(player: Player):
        return {
            "i_decision": player.i_decision,
            "inv1_4": [player.inv1, player.inv2, player.inv3, player.inv4],
            "inv5_8": [
                player.field_maybe_none("inv5"),
                player.field_maybe_none("inv6"),
                player.field_maybe_none("inv7"),
                player.field_maybe_none("inv8"),
            ],
        }


class InvestmentDecision8(Page):
    form_model = "player"
    form_fields = ["inv8"]

    def is_displayed(player: Player):
        return player.inv4 == 10

    def vars_for_template(player: Player):
        return {
            "i_decision": player.i_decision,
            "inv1_4": [player.inv1, player.inv2, player.inv3, player.inv4],
            "inv5_8": [
                player.field_maybe_none("inv5"),
                player.field_maybe_none("inv6"),
                player.field_maybe_none("inv7"),
                player.field_maybe_none("inv8"),
            ],
        }


# Création de page_sequence

intros_1_4 = [InvestmentIntro1, InvestmentIntro2, InvestmentIntro3, InvestmentIntro4]
decisions_1_4 = [
    InvestmentDecision1,
    InvestmentDecision2,
    InvestmentDecision3,
    InvestmentDecision4,
]

page_sequence = [
    GeneralInfo,
    CountDigitTask,
    TaskSuccess,
]
for intro, decision in zip(intros_1_4, decisions_1_4):
    page_sequence.extend([intro, decision, InvestmentConfirm])

for page in [
    InvestmentDecision5,
    InvestmentDecision6,
    InvestmentDecision7,
    InvestmentDecision8,
]:
    page_sequence.extend([page, InvestmentConfirm])
