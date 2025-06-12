from otree.api import *
import random

doc = """
App oTree : risk_aversion

Description : 
- une tâche rémunérée qui permet de gagner C.ENDOWMENT jetons
- une série de jeux de décisions où le hasard joue un rôle
- une seule des décisions est tirée au sort pour déterminer le gain ou la perte.

Auteur : Matthieu Comme (LEFMI)
Version : oTree 5+
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
    NB_BOULES = 60  # nombre total de boules dans l'urne


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # chiffre à compter lors de la tâche, généré dans GeneralInfo
    target_digit = models.IntegerField(initial=0)
    pi_count = models.IntegerField(label="Combien de fois ce chiffre apparaît-il ?")

    # compteur suivant l'avancée dans les decisions
    i_decision = models.IntegerField(initial=1)
    # indice de la décision réellement choisie
    i_final = models.IntegerField(initial=-1)

    # Sommes investies à chaque décision
    inv1 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=-1,
        label="Je décide d'investir :",
    )
    inv2 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=-1,
        label="Je décide d'investir :",
    )
    inv3 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=-1,
        label="Je décide d'investir :",
    )
    inv4 = models.IntegerField(
        choices=[(i, str(i)) for i in range(0, C.MAX_INVESTMENT + 1)],
        initial=-1,
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
    chosen_decision = models.IntegerField(
        initial=0
    )  # indice relatif de la décision tirée au sort
    ball_color = models.StringField(initial="")  # couleur de la boule
    profit = models.CurrencyField(initial=0)  # profit décision

    # retourne le numéro de la décision, prend en compte les décisions non affichées
    def i_visible(self, indice=None) -> int:
        i = self.i_decision if indice is None else indice

        # Conditions d'affichage des décisions 5 à 8
        condition1 = self.inv1 == C.MAX_INVESTMENT
        condition2 = self.inv2 == C.MAX_INVESTMENT
        condition3 = self.inv3 == 0
        condition4 = self.inv4 == 0
        result = 4  # la décision 4 est la dernière obligatoire

        match i:
            case 5:
                result += condition1
            case 6:
                result += condition1 + condition2
            case 7:
                result += condition1 + condition2 + condition3
            case 8:
                result += condition1 + condition2 + condition3 + condition4
            case _:
                result = i

        return result

    # conserve les infos importantes concernant la décision tirée au sort pour les afficher à la toute fin de l'expérience
    def set_participant_vars(self):
        vars = self.participant.vars
        vars["i_decision"] = self.i_visible(self.i_final)
        vars["invested"] = getattr(self, f"inv{self.i_final}")
        vars["ball_color"] = self.ball_color
        vars["profit"] = self.profit
        vars["payoff"] = self.payoff


# ----- FONCTIONS -----


# logique d'affichage : vrai si décision 1 à 4, ou respecte les conditions pour 5 à 8, faux sinon
def display_logic(player: Player) -> bool:
    i = player.i_decision
    max = C.MAX_INVESTMENT
    result = (
        i <= 4
        or (i == 5 and player.inv1 == max)
        or (i == 6 and player.inv2 == max)
        or (i == 7 and player.inv3 == 0)
        or (i == 8 and player.inv4 == 0)
    )
    return result


# utilisée pour debugger
def getTemplate(player: Player) -> dict:
    return {
        "participant.payoff": player.participant.payoff,
        "i_decision": player.i_decision,
        "i_visible": player.i_visible(),
        "i_final": player.i_final,
        "inv1_4": [player.inv1, player.inv2, player.inv3, player.inv4],
        "inv5_8": [
            player.field_maybe_none("inv5"),
            player.field_maybe_none("inv6"),
            player.field_maybe_none("inv7"),
            player.field_maybe_none("inv8"),
        ],
    }


# retourne la couleur de la boule tirée au hasard
def getBallColor(is_blue: bool) -> str:
    i = random.randint(0, (1 + is_blue))
    if i == 0:
        result = "yellow"
    elif i == 1:
        result = "purple"
    else:
        result = "blue"
    return result


# retourne l'indice de la décision tirée au sort
def getFinalDecision(player: Player) -> int:
    decisions = [
        player.inv1,
        player.inv2,
        player.inv3,
        player.inv4,
        player.field_maybe_none("inv5"),
        player.field_maybe_none("inv6"),
        player.field_maybe_none("inv7"),
        player.field_maybe_none("inv8"),
    ]
    while True:
        i = random.randint(0, 7)
        if decisions[i] is not None:
            break
    return i + 1


# retourne le profit final
def finalProfit(player: Player) -> Currency:
    i = player.i_final = getFinalDecision(player)  # indice de la décision tirée au sort
    invested = getattr(player, f"inv{i}")  # somme investie à cette décision

    # tirage de la boule, bleue uniquement présente si tirage = C
    ball_color = getBallColor(False) if invested != "C" else getBallColor(True)
    profit = 0
    if i == 1 or i == 2:
        profit = profit_1_2(invested, ball_color)
    elif i == 3 or i == 4:
        profit = profit_3_4(invested, ball_color)
    else:
        profit = profit_5_8(i, invested, ball_color)
    player.ball_color = ball_color
    return cu(profit)


# retourne le profit pour les décisions 1-8
def profit_1_2(invested: int, ball_color: str) -> int:
    return 3 * invested if ball_color == "yellow" else -invested


def profit_3_4(invested: int, ball_color: str) -> int:
    kept = C.MAX_INVESTMENT - invested
    return -kept if ball_color == "yellow" else -(3 * invested + kept)


def profit_5_8(i_decision: int, invested: int, ball_color: str) -> int:
    profit = getAbsoluteProfit(invested, ball_color)  # profit positif si i=5|6
    if i_decision == 7 or i_decision == 8:  # sinon profit négatif
        profit *= -1
    return profit


# retourne abs(profit) pour décisions 5-8
def getAbsoluteProfit(invested: str, ball_color: str) -> int:
    n = C.MAX_INVESTMENT

    match invested:
        case "A":
            result = n
        case "B":
            result = n // 2 if ball_color == "yellow" else (n * 3) // 2
        case "C":
            if ball_color == "yellow":
                result = n // 2
            elif ball_color == "purple":
                result = n
            else:
                result = (n * 3) // 2
        case "D":
            result = 0 if ball_color == "yellow" else n * 2

    return result


# retourne la balise pour l'emoji de boule
def get_ball_emoji(color) -> str:
    return f"<span class='ball {color}'></span>"


# les 3 fonctions suivantes servent à la mise en page des décisions 5-8
def getLiItems(known: bool) -> list:
    if known:
        n = C.NB_BOULES
        result = [
            f"Urne avec {n} {get_ball_emoji("yellow")} : vous êtes certain de tirer une boule {get_ball_emoji("yellow")}.",
            f"Urne avec {n//2} {get_ball_emoji("yellow")} et {n//2} {get_ball_emoji("purple")} : vous avez 1 chance sur 2 de tirer l’une des 2 couleurs.",
            f"Urne avec {n//3} {get_ball_emoji("yellow")}, {n//3} {get_ball_emoji("purple")} et {n//3} {get_ball_emoji("blue")} : vous avez 1 chance sur 3 de tirer l’une des 3 couleurs.",
        ]
    else:
        result = [
            f"Urne avec {get_ball_emoji("yellow")} : vous êtes certain de tirer une boule {get_ball_emoji("yellow")}.",
            f"Urne avec {get_ball_emoji("yellow")} et {get_ball_emoji("purple")} : vous ne connaissez pas vos chances de tirer chacune des 2 couleurs.",
            f"Urne avec {get_ball_emoji("yellow")}, {get_ball_emoji("purple")} et {get_ball_emoji("blue")} : vous ne connaissez pas vos chances de tirer chacune des 3 couleurs.",
        ]
    return result


# retourne les résultats des tirages 5 à 8 en adaptant si c'est un gain ou une perte de jetons
def getResults(win: bool) -> list:
    n = C.MAX_INVESTMENT
    if win:
        word = "gagnez"
    else:
        word = "perdez"

    return [
        f"Vous {word} {n} jetons",
        f"Boule {get_ball_emoji("yellow")} → vous {word} {n//2} jetons<br>Boule {get_ball_emoji("purple")}→ vous {word} {n*3//2} jetons",
        f"Boule {get_ball_emoji("yellow")} → vous {word} {n//2} jetons<br>Boule {get_ball_emoji("purple")}→ vous {word} {n} jetons<br>Boule {get_ball_emoji("blue")} → vous {word} {n*3//2} jetons",
        f"Boule {get_ball_emoji("yellow")} → vous {word} 0 jeton<br>Boule {get_ball_emoji("purple")}→ vous {word} {n*2} jetons",
    ]


# retourne le contenu des urnes, prend en compte s'il est connu ou non
def getBoxes(known: bool) -> list:
    n = demi = tier = ""
    if known:
        n = C.NB_BOULES
        demi = n // 2
        tier = n // 3

    return [
        f"{n} boules {get_ball_emoji("yellow")}",
        f"{demi} boules {get_ball_emoji("yellow")}<br>{demi} boules {get_ball_emoji("purple")}",
        f"{tier} boules {get_ball_emoji("yellow")}<br>{tier} boules {get_ball_emoji("purple")}<br>{tier} boules {get_ball_emoji("blue")}",
        f"{demi} boules {get_ball_emoji("yellow")}<br>{demi} boules {get_ball_emoji("purple")}",
    ]


# ----- PAGES -----


class CountDigitTask(Page):
    form_model = "player"
    form_fields = ["pi_count"]

    @staticmethod
    def error_message(player: Player, values):
        correct_count = C.PI_DIGITS.count(str(player.target_digit))
        if values["pi_count"] != correct_count:
            return f"Incorrect. Réessayez."

    def vars_for_template(player: Player):
        return getTemplate(player) | dict(
            pi_digits=C.PI_DIGITS,
            digit=player.target_digit,
        )

    def before_next_page(player, timeout_happened):
        player.payoff = C.ENDOWMENT


class GeneralInfo(Page):
    # Génère aléatoirement le chiffre à compter
    # @staticmethod
    # def before_next_page(player: Player, timeout_happened):
    #    player.target_digit = random.randint(0, 9)

    def vars_for_template(player):
        return {
            "etape": "la mesure d'aversion au risque et à l'ambiguité",
        }


class TaskSuccess(Page):
    pass


class InvestmentConfirm(Page):

    def is_displayed(player: Player):
        result = display_logic(player)
        if not result:  # incrémente ici car on ne passera pas par before_next_page
            player.i_decision += 1
        return result

    def before_next_page(player: Player, timeout_happened):
        player.i_decision += 1

    def vars_for_template(player: Player):
        return getTemplate(player)


class InvestmentDecision1_4(Page):
    form_model = "player"

    def get_form_fields(player: Player):
        i = str(player.i_decision)
        return ["inv" + i]

    def vars_for_template(player: Player):
        return getTemplate(player)


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
        return display_logic(player)

    # pour construire les tableaux
    def vars_for_template(player: Player):
        match player.i_decision:
            case 5:
                known = True
                win = True
            case 6:
                known = False
                win = True
            case 7:
                known = True
                win = False
            case 8:
                known = False
                win = False

        return getTemplate(player) | {
            "rows": zip(["A", "B", "C", "D"], getBoxes(known), getResults(win)),
            "li_items": getLiItems(known),
        }


class TirageFinal(Page):

    def vars_for_template(player: Player):

        return getTemplate(player) | {"profit": player.profit}

    def before_next_page(player: Player, timeout_happened):
        player.profit = finalProfit(player)
        player.payoff += player.profit


class Fin(Page):
    # pour essayer plusieurs tirages consécutifs
    # def is_displayed(player: Player):
    # player.profit = finalProfit(player)
    # player.payoff += player.profit
    # return True

    def vars_for_template(player: Player):
        return {
            "i_final": player.i_final,
            "i_visible": player.i_visible(player.i_final),
            "invested": getattr(player, f"inv{player.i_final}"),
            "ball_color": player.ball_color,
            "profit": player.profit,
            "payoff": player.payoff,
            "participant.payoff": player.participant.payoff,
        }

    def before_next_page(player: Player, timeout_happened):
        player.set_participant_vars()

    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        index = player.participant.vars["app_index"]
        if index < 3:
            app_to_go = player.participant.vars["app_order"][index]
            player.participant.vars["app_index"] += 1
            return app_to_go


# Création de page_sequence

page_sequence = [
    GeneralInfo,
    CountDigitTask,
    TaskSuccess,
]

# Ajoute les décisions 1-4

intros_1_4 = [InvestmentIntro1, InvestmentIntro2, InvestmentIntro3, InvestmentIntro4]

for intro in intros_1_4:
    page_sequence.extend([intro, InvestmentDecision1_4, InvestmentConfirm])

# Ajoute les décisions 5-8
for i in range(0, 4):
    page_sequence.extend([InvestmentDecision5_8, InvestmentConfirm])

page_sequence.extend([TirageFinal, Fin])
