# extract_link.py
import sys
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://localhost:8000"
SESSION_CODE = sys.argv[1]  # argument passé en ligne de commande


def get_session_wide_link(session_code):
    url = f"{BASE_URL}/SessionStartLinks/{session_code}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a"):
        link = a.get("href", "")
        if "/join/" in link:
            return link

    return "NOT_FOUND"


if __name__ == "__main__":
    print(get_session_wide_link(SESSION_CODE))
