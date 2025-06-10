from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = "questionnaire"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    AI_KNOWLEDGE_CHOICES = [
        [1, "Je ne sais pas du tout ce que c’est"],
        [2, "Je pense savoir ce que c’est"],
        [3, "Je sais de quoi il s’agit"],
        [4, "Je sais précisément de quoi il s’agit"],
    ]

    AGREEMENT_CHOICES = [
        [1, "Pas du tout d’accord"],
        [2, "Plutôt pas d'accord"],
        [3, "ni d'accord ni pas d'accord"],
        [4, "Plutôt d’accord"],
        [5, "Tout à fait d'accord"],
        [6, "Je ne sais pas"],
    ]

    FREQUENCY_CHOICES = [
        [1, "Pas du tout"],
        [2, "Un peu"],
        [3, "Moyennement"],
        [4, "Beaucoup"],
        [5, "Énormément"],
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    player_name = models.StringField(label="Veuillez entrer votre nom")
    go_back = models.BooleanField(initial=False)
    # Q1
    ai_knowledge = models.IntegerField(
        label="À quel point êtes-vous familier avec le terme « intelligence artificielle » ?",
        choices=C.AI_KNOWLEDGE_CHOICES,
        widget=widgets.RadioSelect,
    )

    # Q2 (13 affirmations)
    q2_impact_tasks = models.IntegerField(
        label="...va modifier directement les tâches de nombreux travailleurs",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_dehumanization = models.IntegerField(
        label="...risque de déshumaniser certains services",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_job_loss = models.IntegerField(
        label="...risque de faire perdre leur emploi à de nombreux travailleurs",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_performance = models.IntegerField(
        label="...va rendre les entreprises plus performantes",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_interest = models.IntegerField(
        label="...vous intéresse",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_daily_life = models.IntegerField(
        label="...va améliorer votre quotidien",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_positive_evolution = models.IntegerField(
        label="...est une évolution positive pour la société",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_quebec_worry = models.IntegerField(
        label="...vous inquiète collectivement pour le Québec",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_personal_worry = models.IntegerField(
        label="...vous inquiète personnellement",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_solution_penurie = models.IntegerField(
        label="...est une solution à la pénurie de main-d’œuvre",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_modif_my_tasks = models.IntegerField(
        label="...va modifier directement vos tâches au travail",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_create_jobs = models.IntegerField(
        label="...va créer des emplois",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    q2_lose_my_job = models.IntegerField(
        label="...risque de vous faire perdre votre emploi",
        choices=C.AGREEMENT_CHOICES,
        widget=widgets.RadioSelect,
    )

    # Q3 — Choix multiple simulé par un champ texte (facile)
    q3_sectors = models.StringField(
        label="Quels secteurs bénéficieront le plus de l’IA ? (séparez vos choix par des virgules)"
    )

    # Q4 — Choix multiple simulé par un champ texte
    q4_government_actions = models.StringField(
        label="Quelles actions le gouvernement devrait-il prioriser selon vous ? (séparez vos choix par des virgules)"
    )

    # Q5 — Médias
    q5_tv = models.IntegerField(
        label="Télévision ou radio",
        choices=C.FREQUENCY_CHOICES,
        widget=widgets.RadioSelect,
    )
    q5_websites = models.IntegerField(
        label="Internet : sites Web",
        choices=C.FREQUENCY_CHOICES,
        widget=widgets.RadioSelect,
    )
    q5_social = models.IntegerField(
        label="Internet : réseaux sociaux",
        choices=C.FREQUENCY_CHOICES,
        widget=widgets.RadioSelect,
    )
    q5_journals = models.IntegerField(
        label="Journaux quotidiens/hebdomadaires",
        choices=C.FREQUENCY_CHOICES,
        widget=widgets.RadioSelect,
    )
    q5_freepress = models.IntegerField(
        label="Journaux gratuits (métro, local)",
        choices=C.FREQUENCY_CHOICES,
        widget=widgets.RadioSelect,
    )


# ==== PAGES ====


class Question1(Page):
    form_model = "player"
    form_fields = ["ai_knowledge"]

    def vars_for_template(player):
        return dict(
            ai_definition="On entend par intelligence artificielle un programme informatique ou un robot capable de réfléchir et penser par lui-même au-delà de sa programmation initiale (véhicule autonome, robot médical, montre intelligente, etc.)."
        )


class Question2(Page):
    form_model = "player"
    form_fields = [
        "q2_impact_tasks",
        "q2_dehumanization",
        "q2_job_loss",
        "q2_performance",
        "q2_interest",
        "q2_daily_life",
        "q2_positive_evolution",
        "q2_quebec_worry",
        "q2_personal_worry",
        "q2_solution_penurie",
        "q2_modif_my_tasks",
        "q2_create_jobs",
        "q2_lose_my_job",
    ]

    def before_next_page(player, timeout_happened):
        if player.go_back:
            player._index_in_pages -= 2  # retourne 1 page en arrière
            player.go_back = False


class Question3(Page):
    form_model = "player"
    form_fields = ["q3_sectors"]

    def before_next_page(player, timeout_happened):
        if player.go_back:
            player._index_in_pages -= 2  # retourne 1 page en arrière
            player.go_back = False

    def vars_for_template(player):
        return dict(
            choices=[
                (1, "La domotique"),
                (2, "Le secteur manufacturier"),
                (3, "Le secteur médical"),
                (4, "Le transport"),
                (5, "Le secteur de l’énergie"),
                (6, "Le commerce et la distribution"),
                (7, "Les services clients"),
                (8, "Le secteur des banques"),
                (9, "Le secteur des assurances"),
                (10, "Je ne sais pas"),
                (11, "Aucun"),
            ]
        )


class Question4(Page):
    form_model = "player"
    form_fields = ["q4_government_actions"]

    def before_next_page(player, timeout_happened):
        if player.go_back:
            player._index_in_pages -= 2  # retourne 1 page en arrière
            player.go_back = False

    def vars_for_template(player):
        return dict(
            actions=[
                "Venir en aide aux employés licenciés à cause des nouvelles technologies numériques",
                "Veiller à la protection des données personnelles",
                "Encadrer le développement de l’IA au niveau éthique",
                "Financer la formation des employés aux nouvelles technologies",
                "Informer davantage la population sur les nouvelles technologies",
                "Investir dans la recherche en IA",
                "Éduquer au numérique (programmes d’éducation)",
                "Ne pas intervenir du tout",
            ]
        )


class Question5(Page):
    form_model = "player"
    form_fields = ["q5_tv", "q5_websites", "q5_social", "q5_journals", "q5_freepress"]

    def before_next_page(player, timeout_happened):
        if player.go_back:
            player._index_in_pages -= 2  # retourne 1 page en arrière
            player.go_back = False


class Login(Page):
    form_model = "player"
    form_fields = ["player_name"]


class Welcome(Page):
    # Cette page affichera le message de bienvenue avec le nom du joueur
    pass


class Conclusion(Page):
    @staticmethod
    def app_after_this_page(player: Player, upcoming_apps):
        index = player.participant.vars["app_index"]
        if index < 3:
            app_to_go = player.participant.vars["app_order"][index]
            player.participant.vars["app_index"] += 1
            return app_to_go


page_sequence = [
    Welcome,
    Question1,
    Question2,
    Question3,
    Question4,
    Question5,
    Conclusion,
]
