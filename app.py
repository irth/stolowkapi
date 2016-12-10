from bs4 import BeautifulSoup
import urllib.request

from flask import Flask
import json


def get_menu():
    with urllib.request.urlopen("http://www.zs23.wroclaw.pl/internat/jadlospis.php") as url:
        html_doc = url.read()

    soup = BeautifulSoup(html_doc, 'html.parser')
    ignore = True
    menu = {}
    for tr in soup.table.find_all("tr"):
        if tr.get_text().strip() in ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]:
            ignore = False
            weekday = tr.get_text().strip()
            continue
        if ignore or tr.get_text().strip() == "":
            continue
        day = []
        for bobiad in tr.find_all("td", class_="bobiad"):
            if bobiad.get_text().strip() != '':
                day.append(bobiad.get_text().strip())
        menu[weekday] = day
    return menu


app = Flask(__name__)


@app.route("/")
def root():
    return "Stolowka 23 menu API. Try /menu.json\n"


@app.route("/menu.json")
def menu():
    return json.dumps(get_menu()) + '\n'


if __name__ == '__main__':
    app.run('0.0.0.0')
