from otree.api import *

# Options de loterie pour chaque décision
class C():
    DECISION_1_LOTTERIES = {
        "A": {
            "description": "100% de chances de gagner 10 jetons",
            "probs": [1.0, 0.0],
            "payouts": [10, 0],
        },
        "B": {
            "description": "50% de chances de gagner 8 jetons\n50% de chances de gagner 13 jetons",
            "probs": [0.5, 0.5],
            "payouts": [8, 13],
        },
        "C": {
            "description": "50% de chances de gagner 6 jetons\n50% de chances de gagner 16 jetons",
            "probs": [0.5, 0.5],
            "payouts": [6, 16],
        },
        "D": {
            "description": "50% de chances de gagner 4 jetons\n50% de chances de gagner 19 jetons",
            "probs": [0.5, 0.5],
            "payouts": [4, 19],
        },
        "E": {
            "description": "50% de chances de gagner 2 jetons\n50% de chances de gagner 20 jetons",
            "probs": [0.5, 0.5],
            "payouts": [2, 20],
        },
        "F": {
            "description": "50% de chances de gagner 0 jetons\n50% de chances de gagner 25 jetons",
            "probs": [0.5, 0.5],
            "payouts": [0, 25],
        },
    }

    DECISION_2_LOTTERIES = {
        "A": {
            "description": "100% de chances de perdre 10 jetons",
            "probs": [1.0, 0.0],
            "payouts": [-10, 0],
        },
        "B": {
            "description": "50% de chances de perdre 8 jetons\n50% de chances de perdre 13 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-8, -13],
        },
        "C": {
            "description": "50% de chances de perdre 6 jetons\n50% de chances de perdre 16 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-6, -16],
        },
        "D": {
            "description": "50% de chances de perdre 4 jetons\n50% de chances de perdre 19 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-4, -19],
        },
        "E": {
            "description": "50% de chances de perdre 2 jetons\n50% de chances de perdre 20 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-2, -20],
        },
        "F": {
            "description": "50% de chances de perdre 0 jetons\n50% de chances de perdre 25 jetons",
            "probs": [0.5, 0.5],
            "payouts": [0, -25],
        },
    }

    DECISION_3_LOTTERIES = {
        "A": {
            "description": "50% de chances de gagner 10 jetons",
            "probs": [0.5, 0.5],
            "payouts": [10, 0],
        },
        "B": {
            "description": "50% de chances de gagner 8 jetons\n50% de chances de gagner 13 jetons",
            "probs": [0.5, 0.5],
            "payouts": [8, 13],
        },
        "C": {
            "description": "50% de chances de gagner 6 jetons\n50% de chances de gagner 16 jetons",
            "probs": [0.5, 0.5],
            "payouts": [6, 16],
        },
        "D": {
            "description": "50% de chances de gagner 4 jetons\n50% de chances de gagner 19 jetons",
            "probs": [0.5, 0.5],
            "payouts": [4, 19],
        },
        "E": {
            "description": "50% de chances de gagner 2 jetons\n50% de chances de gagner 20 jetons",
            "probs": [0.5, 0.5],
            "payouts": [2, 20],
        },
        "F": {
            "description": "50% de chances de gagner 0 jetons\n50% de chances de gagner 25 jetons",
            "probs": [0.5, 0.5],
            "payouts": [0, 25],
        },
    }
    DECISION_F_FOLLOWUP = {
        "A": {"description": "Gagner 10 jetons", "probs": [1.0], "payouts": [10]},
        "B": {
            "description": "1 chance sur 2 de gagner 5 ou 15 jetons",
            "probs": [0.5, 0.5],
            "payouts": [5, 15],
        },
        "C": {
            "description": "1 chance sur 3 de gagner 5, 10 ou 15 jetons",
            "probs": [1 / 3, 1 / 3, 1 / 3],
            "payouts": [5, 10, 15],
        },
        "D": {
            "description": "1 chance sur 2 de gagner 0 ou 20 jetons",
            "probs": [0.5, 0.5],
            "payouts": [0, 20],
        },
    }

    DECISION_4_LOTTERIES = {
        "A": {
            "description": "100% de chances de perdre 10 jetons",
            "probs": [1.0, 0.0],
            "payouts": [-10, 0],
        },
        "B": {
            "description": "50% de chances de perdre 8 jetons\n50% de chances de perdre 13 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-8, -13],
        },
        "C": {
            "description": "50% de chances de perdre 6 jetons\n50% de chances de perdre 16 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-6, -16],
        },
        "D": {
            "description": "50% de chances de perdre 4 jetons\n50% de chances de perdre 19 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-4, -19],
        },
        "E": {
            "description": "50% de chances de perdre 2 jetons\n50% de chances de perdre 20 jetons",
            "probs": [0.5, 0.5],
            "payouts": [-2, -20],
        },
        "F": {
            "description": "50% de chances de perdre 0 jetons\n50% de chances de perdre 25 jetons",
            "probs": [0.5, 0.5],
            "payouts": [0, -25],
        },
    }
    # 1 si l'individu a investi 10 jetons à la décision 1

    # Choix de loteries
    # decision_1 = models.StringField(
    #     label="Décision 1",
    #     choices=["A", "B", "C", "D", "E", "F"],
    #     widget=widgets.RadioSelect,
    # )
    # decision_2 = models.StringField(
    #     label="Décision 2",
    #     choices=["A", "B", "C", "D", "E", "F"],
    #     widget=widgets.RadioSelect,
    # )
    # decision_3 = models.StringField(
    #     label="Décision 3",
    #     choices=["A", "B", "C", "D", "E", "F"],
    #     widget=widgets.RadioSelect,
    # )
    # decision_4 = models.StringField(
    #     label="Décision 4",
    #     choices=["A", "B", "C", "D", "E", "F"],
    #     widget=widgets.RadioSelect,
    # )
    # decision_f_followup = models.StringField(
    #     label="Choix de loterie supplémentaire après F",
    #     choices=["A", "B", "C", "D"],
    #     widget=widgets.RadioSelect,
    #     blank=True,
    # )

    # # Paiement
    # chosen_decision = models.IntegerField()
    # lottery_result = models.FloatField()  # Résultat du tirage aléatoire (0-1)
    # chosen_lottery = models.StringField()  # Lottery choisie (A, B, C, D, E, F)
    # lottery_outcome = models.CurrencyField()  # Résultat de la loterie
    # final_payoff = models.CurrencyField()  # Paiement final
    # is_gain = models.BooleanField()  # Si vrai: gain, si faux: perte


# === Pages ===


# class Instructions(Page):
#     @staticmethod
#     def before_next_page(player, timeout_happened):
#         # Assign a random digit when moving from Instructions to CountDigitIntro
#         player.target_digit = random.randint(0, 9)

#class InvestmentInfo(Page):
 #   pass

    # class Investment1(Page):
    #     form_model = "player"
    #     form_fields = ["decision_1"]

    #     def vars_for_template(player):
    #         return {
    #             "lotteries": C.DECISION_1_LOTTERIES,
    #             "decision_number": 1,
    #             "is_gain": True,
    #         }

    # class DecisionFFollowup(Page):
    #     form_model = "player"
    #     form_fields = ["decision_f_followup"]

    #     @staticmethod
    #     def is_displayed(player):
    #         return player.decision_1 == "F"

    #     def vars_for_template(player):
    #         return {
    #             "options": {
    #                 "A": "Gagner 10 jetons",
    #                 "B": "1 chance sur 2 de gagner 5 jetons, 1 chance sur 2 de gagner 15 jetons",
    #                 "C": "1 chance sur 3 de gagner 5, 10, ou 15 jetons",
    #                 "D": "1 chance sur 2 de gagner 0 jeton, 1 chance sur 2 de gagner 20 jetons",
    #             }
    #         }

    # class Investment2(Page):
    #     form_model = "player"
    #     form_fields = ["decision_2"]

    #     def vars_for_template(player):
    #         return {
    #             "lotteries": C.DECISION_2_LOTTERIES,
    #             "decision_number": 2,
    #             "is_gain": False,
    #         }

    # class Investment3(Page):
    #     form_model = "player"
    #     form_fields = ["decision_3"]

    #     def vars_for_template(player):
    #         return {
    #             "lotteries": C.DECISION_3_LOTTERIES,
    #             "decision_number": 3,
    #             "is_gain": True,
    #         }

    # class Investment4(Page):
    #     form_model = "player"
    #     form_fields = ["decision_4"]

    #     def vars_for_template(player):
    #         return {
    #             "lotteries": C.DECISION_4_LOTTERIES,
    #             "decision_number": 4,
    #             "is_gain": False,
    #         }

    # class LotteryDraw(Page):
    #     def before_next_page(player, timeout_happened):
    #         # Si le joueur a choisi F à la décision 1
    #         if player.decision_1 == "F" and player.decision_f_followup:
    #             player.chosen_decision = 0  # 0 indique que c’est la décision spéciale
    #             player.chosen_lottery = player.decision_f_followup
    #             lottery_info = C.DECISION_F_FOLLOWUP[player.chosen_lottery]
    #             player.is_gain = True
    #         else:
    #             # Choisir une décision au hasard parmi les décisions classiques (1 à 4)
    #             decision_number = random.randint(1, 4)
    #             player.chosen_decision = decision_number

    #             if decision_number == 1:
    #                 chosen_lottery = player.decision_1
    #                 lottery_info = C.DECISION_1_LOTTERIES[chosen_lottery]
    #                 player.is_gain = True
    #             elif decision_number == 2:
    #                 chosen_lottery = player.decision_2
    #                 lottery_info = C.DECISION_2_LOTTERIES[chosen_lottery]
    #                 player.is_gain = False
    #             elif decision_number == 3:
    #                 chosen_lottery = player.decision_3
    #                 lottery_info = C.DECISION_3_LOTTERIES[chosen_lottery]
    #                 player.is_gain = True
    #             else:
    #                 chosen_lottery = player.decision_4
    #                 lottery_info = C.DECISION_4_LOTTERIES[chosen_lottery]
    #                 player.is_gain = False

    #             player.chosen_lottery = chosen_lottery

    #         # Tirage au sort selon la loterie choisie
    #         probs = lottery_info["probs"]
    #         payouts = lottery_info["payouts"]

    #         r = random.random()
    #         cumulative = 0
    #         for prob, payout in zip(probs, payouts):
    #             cumulative += prob
    #             if r <= cumulative:
    #                 player.lottery_outcome = cu(payout)
    #                 break

    #         # Paiement final
    #         player.lottery_result = r
    #         player.final_payoff = C.ENDOWMENT + player.lottery_outcome

    #     def vars_for_template(player):
    #         if player.decision_1 == "F" and player.decision_f_followup:
    #             # Il n'y a qu'une seule décision possible à tirer : la spéciale
    #             return dict(
    #                 decisions_made=["Décision spéciale liée à l’option F"],
    #                 is_special_followup=True,
    #             )
    #         else:
    #             return dict(
    #                 decisions_made=[
    #                     f"Décision 1: {player.decision_1}",
    #                     f"Décision 2: {player.decision_2}",
    #                     f"Décision 3: {player.decision_3}",
    #                     f"Décision 4: {player.decision_4}",
    #                 ],
    #                 is_special_followup=False,
    #             )

    # class Results(Page):
    # def vars_for_template(player):
    #     if player.chosen_decision == 0:
    #         lottery_info = C.DECISION_F_FOLLOWUP[player.chosen_lottery]
    #     elif player.chosen_decision == 1:
    #         lottery_info = C.DECISION_1_LOTTERIES[player.chosen_lottery]
    #     elif player.chosen_decision == 2:
    #         lottery_info = C.DECISION_2_LOTTERIES[player.chosen_lottery]
    #     elif player.chosen_decision == 3:
    #         lottery_info = C.DECISION_3_LOTTERIES[player.chosen_lottery]
    #     else:
    #         lottery_info = C.DECISION_4_LOTTERIES[player.chosen_lottery]

    #     # Formater les nombres pour l'affichage
    #     lottery_result_formatted = f"{player.lottery_result:.4f}"
    #     threshold_formatted = f"{lottery_info['probs'][0]:.1f}"

    #     return {
    #         "initial_endowment": C.ENDOWMENT,
    #         "lottery_outcome": player.lottery_outcome,
    #         "payoff": player.final_payoff,
    #         "chosen_decision": player.chosen_decision,
    #         "chosen_lottery": player.chosen_lottery,
    #         "lottery_desc": lottery_info["description"],
    #         "lottery_result": player.lottery_result,  # Valeur originale pour les comparaisons
    #         "lottery_result_formatted": lottery_result_formatted,  # Valeur formatée pour l'affichage
    #         "lottery_threshold": lottery_info["probs"][0],  # Valeur originale
    #         "threshold_formatted": threshold_formatted,  # Valeur formatée
    #         "high_outcome": cu(lottery_info["payouts"][0]),
    #         "low_outcome": cu(lottery_info["payouts"][1]),
    #         "is_gain": player.is_gain,
    #         # Ajout d'indicateurs clairs pour le template
    #         "won_high": player.lottery_result <= lottery_info["probs"][0],
    #     }

class CountDigitIntro(Page):
    def vars_for_template(player):
        return dict(
            ENDOWMENT = C.ENDOWMENT,
            pi_digits=C.PI_DIGITS,
            digit=player.target_digit,
        )
        
class TaskSuccess(Page):
     def before_next_page(player, timeout_happened):
            player.payoff = C.ENDOWMENT