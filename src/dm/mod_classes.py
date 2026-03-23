import json
import os

import requests
from bs4 import BeautifulSoup

from dm.config import settings
from dm.utils import choix_menu

class Menu:

    donnees = []

    def __init__(self, nom, url, description, formats):
        self.nom = nom
        self.url = url
        self.description = description
        self.formats = formats

    def __str__(self):
        return f'{self.nom}\n{self.url}'

    def executer(self):
        self.afficher_donnees()
        option = 1
        while (True):
            if not settings.MODE_AUTONOME:
                fmts = ", ".join(f"{i+1} - {f['format']}" for i, f in enumerate(donnees))
                option = choix_menu(f'Saisir le format à télécharger ({fmts}):')
            if option < 1 or option > len(donnees):
                break
            self.download(option)
            option = option + 1


    def afficher_donnees(self):
        response = requests.get(self.url, headers=settings.HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        global donnees
        donnees = get_donnees(soup)

        for i, d in enumerate(donnees, start=1):
            print(f"{i:02d}. {d['format']}")
            print(f"     Description          : {d['description']}")
            print(f"     Dernière modification: {d['date_modification']}")
            print(f"     URL     : {d['url']}")
            print()


    def download(self, index_format):
        if index_format < 1 or index_format > len(donnees):
            return
        #for i, d in enumerate(donnees, start=1):
        #print(f"{i:02d}. {d['format']}")
        d = donnees[index_format - 1]
        dir = self.url.split("/")[-1]
        fichier = dir + '/' + d['url'].split("/")[-1]
        #print(f'dir: {dir}  fichier: {fichier})
        if d['format'] == 'WEB' or d['format'] == 'HTML':
            print(f'Sauter download - Format {d['format']} {fichier}')
            return

        self.create_dir(dir)
        response = requests.get(d['url'])
        if response.status_code == 200:
            with open(fichier, "wb") as f:
                f.write(response.content)
                print(f"Fichier téléchargé: {fichier}")
        else:
            print(f"Échec lors du téléchargement: {fichier} - {response.status_code}")
            print(f"URL: {d['url']}")


    def create_dir(self, dir):
        dir_current = os.getcwd()
        nouveau_dir = os.path.join(dir_current, dir)
        os.makedirs(nouveau_dir, exist_ok=True)


def get_format(item):
    span = item.find("span", class_=lambda c: c and "badge" in c)
    return span.get_text(strip=True)


def get_url(item):
    link = item.find("a")
    return link.get("href", "") if link else ""


def get_description(item):
    div = item.find("div", class_=lambda c: c and "list-group-item-title" in c)
    if not div:
        return ""
    return div.get_text()


def get_date_modification(item):
    div = item.find("div", class_=lambda c: c and "list-group-item-infos" in c)
    if not div:
        return ""
    # return div.get_text(strip=True)
    return div.contents[2].get_text(strip=True)


def get_donnees(soup):
    div_list = soup.find(
        "div",
        class_=lambda c: c and "list-group-teaser" in c and "list-group-complex" in c
    )
    if not div_list:
        raise ValueError("C'est grave! La balise div.list-group-teaser n'a été pas trouvé.")

    ressources = []
    for item in div_list.find_all("div", class_="list-group-item", recursive=False):
        ressources.append({
            "format": get_format(item),
            "url": get_url(item),
            "description": get_description(item),
            "date_modification": get_date_modification(item)
        })
    return ressources

