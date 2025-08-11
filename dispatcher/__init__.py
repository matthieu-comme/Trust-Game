import subprocess
from otree.api import *
from otree.session import create_session
import requests
from bs4 import BeautifulSoup


class C(BaseConstants):
    NAME_IN_URL = "dispatcher"
    PLAYERS_PER_GROUP = 16
    NUM_ROUNDS = 1
    NUM_APPS = 3
    BASE_URL = "http://localhost:8000"
    USERNAME = "admin"
    PASSWORD = "admin"
    # insérer le code du session-wide link, et non le code de la session
    CODE_GROUPE_1 = "vudisufe"
    CODE_GROUPE_2 = "	tafefoho"
    CODE_GROUPE_3 = "semitolu"

    """
    PERMUTATIONS = [
        # ("trust_game", "questionnaire", "risk_aversion"), permutation test tg
        # ("risk_aversion", "trust_game", "questionnaire"),
        ("questionnaire", "risk_aversion", "trust_game"),  # Groupe 1
        ("risk_aversion", "questionnaire", "trust_game"),  # Groupe 2
        ("questionnaire", "trust_game", "risk_aversion"),  # Groupe 3
    ]
    """


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # is_session_created = models.BooleanField(initial=False)
    group_number = models.IntegerField()


# FONCTIONS

"""

def get_all_link_codes(session_code: str) -> list:
    print("0")
    s = requests.Session()

    # si connexion à otree nécessaire
    # s.post(f'{C.BASE_URL}/accounts/login/', data={'username': C.USERNAME,'password': C.PASSWORD,})
    print("1")
    url = f"{C.BASE_URL}/SessionStartLinks/{session_code}"
    print("URL =", url)
    r = s.get(url)
    print("2")

    soup = BeautifulSoup(r.text, "html.parser")
    print("3")

    result = []
    for a in soup.select(".participant-link"):
        link_code = a.getText().split("/")[-1]
        result.append(link_code)
    print("4")

    return result



def create_group_session(player: Player):
    n = player.group_number
    session = create_session(
        session_config_name=f"groupe_{n}",
        num_participants=player.session.num_participants // 3,
    )
    code = session.code
    print(f"Session code : {code}")
    # print(get_session_wide_link(session.code))
    result = subprocess.run(
        ["python", "extract_link.py", code], capture_output=True, text=True, timeout=5
    )
    session_link = result.stdout.strip()
    print("enfin !", session_link)

    player.participant.vars["session_code"] = code
    player.is_session_created = True


def get_session_code(player: Player) -> str:
    i = player.group_number
    participant = next(
        p for p in player.session.get_participants() if p.id_in_session == i
    )
    code = participant.vars["session_code"]
    return code

"""


def get_code(player: Player):
    n = player.group_number
    if n == 1:
        code = C.CODE_GROUPE_1
    elif n == 2:
        code = C.CODE_GROUPE_2
    else:
        code = C.CODE_GROUPE_3

    return code.strip()


class Welcome(Page):

    def is_displayed(player: Player):
        # répartit les joueurs 1 par 1 dans les groupes 1 à 3
        player.group_number = (player.participant.id_in_session - 1) % 3 + 1

        # id = player.participant.id_in_session
        # if (id == 1 or id == 2 or id == 3) and not player.is_session_created:
        #    create_group_session(player)

        return True

    def vars_for_template(player: Player):
        return {
            # "player_vars": player.participant.vars,
            "group_number": player.group_number,
            # "code": get_session_code(player),
            # "total_participants": len(player.session.get_participants()),
            # "total_players": len(player.subsession.get_players()),
            # "players_in_group": len(player.group.get_players()),
        }

    def before_next_page(player: Player, timeout_happened):
        pass


class Dispatch(Page):

    @staticmethod
    def vars_for_template(player: Player):
        code = get_code(player)
        return {
            "player_vars": player.participant.vars,
            "group_number": player.group_number,
            "code": code,
            "link": f'href="{C.BASE_URL}/join/{code}"',
        }


page_sequence = [Welcome, Dispatch]
