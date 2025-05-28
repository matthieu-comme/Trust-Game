from os import environ


SESSION_CONFIGS = [
    dict(
        name="experiment_randomized",
        display_name="Expérience randomisée par groupe",
        num_demo_participants=60,
        app_sequence=["dispatcher", "questionnaire", "trust_game", "risk_aversion"],
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
