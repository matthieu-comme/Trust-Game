from os import environ

PLAYERS_PER_GROUP = 20
SESSION_CONFIGS = [
    dict(
        name="chatgpt",
        display_name="Test ChatGPT",
        num_demo_participants=2,
        app_sequence=["chatgpt"],
    ),
    dict(
        name="risk_aversion",
        display_name="Mesure d'aversion au risque",
        num_demo_participants=1,
        app_sequence=["risk_aversion"],
    ),
    dict(
        name="trust_game_test",
        display_name="Trust Game Classique",
        num_demo_participants=2,
        app_sequence=["trust_game"],
    ),
    dict(
        name="test_questionnaire",
        display_name="Test Questionnaire IA",
        num_demo_participants=20,
        app_sequence=["questionnaire"],
    ),
    dict(
        name="dispatcher_2",
        display_name="Dispatcher 2",
        num_demo_participants=3 * PLAYERS_PER_GROUP,
        app_sequence=["dispatcher_2"],
    ),
    dict(
        name="groupe_1",
        display_name="Groupe 1",
        num_demo_participants=PLAYERS_PER_GROUP,
        app_sequence=["questionnaire", "risk_aversion", "trust_game"],
    ),
    dict(
        name="groupe_2",
        display_name="Groupe 2",
        num_demo_participants=PLAYERS_PER_GROUP,
        app_sequence=["risk_aversion", "questionnaire", "trust_game"],
    ),
    dict(
        name="groupe_3",
        display_name="Groupe 3",
        num_demo_participants=PLAYERS_PER_GROUP,
        app_sequence=["questionnaire", "trust_game", "risk_aversion"],
    ),
    dict(
        name="experiment_randomized",
        display_name="Expérience randomisée par groupe",
        num_demo_participants=3 * PLAYERS_PER_GROUP,
        app_sequence=["dispatcher", "questionnaire", "trust_game", "risk_aversion"],
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "USD"
USE_POINTS = True

ROOMS = [
    dict(
        name="econ101",
        display_name="Econ 101 class",
        participant_label_file="_rooms/econ101.txt",
    ),
    dict(name="live_demo", display_name="Room for live demo (no participant labels)"),
]

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""

# DEBUG = False

SECRET_KEY = "9819358673787"
LANGUAGE_CODE = "fr"
USE_POINTS = False
REAL_WORLD_CURRENCY_CODE = "jetons"

INSTALLED_APPS = ["otree", "dispatcher", "otree.chat"]
