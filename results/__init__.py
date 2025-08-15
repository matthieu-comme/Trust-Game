from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = "results"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    SHOW_UP_FEE = cu(10)
    CONVERSION_RATE = 0.5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    gain_total = models.CurrencyField()
    gain_euros = models.FloatField()


# PAGES
class Intro(Page):
    pass


class Results(Page):
    def vars_for_template(player: Player):
        player.gain_total = C.SHOW_UP_FEE

        vars = player.participant.vars
        gain_risk_aversion = cu(vars["total_risk_aversion"])

        tg_role = vars.get("tg_role")
        vars_tg = {}
        # pour que le module results fonctionne meme sans jouer le tg
        if tg_role:
            endowment = int(vars.get("tg_endowment"))
            mult = int(vars.get("tg_multiplier"))
            sent = int(vars.get("tg_sent"))
            sent_back = int(vars.get("tg_sent_back"))

            if tg_role == "A":
                tg_gain = cu(endowment - sent + sent_back)
            else:
                tg_gain = cu(mult * sent - sent_back)

            player.gain_total += tg_gain

            vars_tg = {
                "tg_endowment": endowment,
                "tg_sent": sent,
                "tg_multiplier": mult,
                "tg_sent_back": sent_back,
                "tg_gain": tg_gain,
            }

        player.gain_total += gain_risk_aversion
        player.gain_euros = round(float(player.gain_total * C.CONVERSION_RATE), 2)

        return {
            "show_up_fee": C.SHOW_UP_FEE,
            "chosen_decision": vars["chosen_decision"],
            "invested": vars["invested"],
            "ball_color": vars["ball_color"],
            "initial_amount": vars["initial_amount"],
            "profit_risk_aversion": vars["profit_risk_aversion"],
            "gain_risk_aversion": gain_risk_aversion,
            "gain_total": player.gain_total,
            "tg_role": tg_role,
            "tg_gain": cu(0),
            "converted_gain": player.gain_euros,
        } | vars_tg


page_sequence = [Intro, Results]
