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
    ENDOWMENT = cu(30)  # somme gagnée à la fin de la tâche
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
    target_digit = models.IntegerField(initial=0)  # chiffre à compter lors de la tâche
    pi_count = models.IntegerField(label="Combien de fois ce chiffre apparaît-il ?")

    i_decision = models.IntegerField(initial=1)

    # Sommes investies à chaque décision
    inv1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv2 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv3 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=0,
        label="Je décide d'investir :",
    )
    inv4 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
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
    def error_message(player: Player, values):
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
            or (i == 7 and player.inv3 == 0)
            or (i == 8 and player.inv4 == 0)
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


class InvestmentDecision1_4(Page):
    form_model = "player"

    def get_form_fields(player: Player):
        i = str(player.i_decision)
        return ["inv" + i]


class InvestmentIntro1(Page):
    pass


class InvestmentIntro2(Page):
    pass


class InvestmentIntro3(Page):
    pass


class InvestmentIntro4(Page):
    pass


class InvestmentDecision5_8(Page):
    form_model = "player"

    def get_form_fields(player: Player):
        i = str(player.i_decision)
        return ["inv" + i]

    def is_displayed(player: Player):
        i = player.i_decision
        max = C.MAX_INVESTMENT
        result = (
            (i == 5 and player.inv1 == max)
            or (i == 6 and player.inv2 == max)
            or (i == 7 and player.inv3 == 0)
            or (i == 8 and player.inv4 == 0)
        )
        if not result:  # incrémente ici car on ne passera pas par confirm
            player.i_decision += 1

        return result

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


class Fin(Page):
    pass


# Création de page_sequence

page_sequence = [
    GeneralInfo,
    CountDigitTask,
    TaskSuccess,
]

# Ajoute les décisions 1 à 4

intros_1_4 = [InvestmentIntro1, InvestmentIntro2, InvestmentIntro3, InvestmentIntro4]

for intro in intros_1_4:
    page_sequence.extend([intro, InvestmentDecision1_4, InvestmentConfirm])

# Ajoute les décisions 5 à 8
for i in range(0, 4):
    page_sequence.extend([InvestmentDecision5_8, InvestmentConfirm])

page_sequence.append(Fin)
