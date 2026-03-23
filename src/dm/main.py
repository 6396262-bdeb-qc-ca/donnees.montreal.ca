import json
import requests
from bs4 import BeautifulSoup

from dm import mod_classes
from dm.config import settings
from dm.utils import choix_menu

BASE_URL = "https://donnees.montreal.ca"
URL = f"{BASE_URL}/group/tourisme-sports-loisirs"

menus = []

def main():
    print(f"Web scraping sur: {URL}\n")

    response = requests.get(URL, headers=settings.HEADERS, timeout=15)

    menus = get_menus(response.text)
    afficher_menus()
    option = 1
    while(True):
        if not settings.MODE_AUTONOME:
            option = choix_menu(f'Saisir une option de Menu (1-{len(menus)}):')
        if option < 1 or option > len(menus):
            break
        print(menus[option - 1])
        menus[option - 1].executer()
        option = option + 1


def get_menus(html):
    soup = BeautifulSoup(html, "html.parser")

    ul = soup.find("ul", class_=lambda c: c and "pt-gutter" in c and "font-open-sans" in c)
    if not ul:
        raise ValueError("La balise <ul class='pt-gutter font-open-sans'> n'a pas trouvé.")

    global menus
    menus = []
    for li in ul.find_all("li", recursive=False):
        h3 = li.find("h3")
        if not h3:
            continue
        link = h3.find("a")
        if not link:
            continue

        href = link.get("href", "")
        menu = mod_classes.Menu(link.get_text(strip=True), BASE_URL + href, get_description(li), get_formats(li))
        menus.append(menu)
    return menus


def get_formats(li_elem):
    # <ul class='mt-2'>
    ul = li_elem.find("ul", class_=lambda c: c and "mt-2" in c)
    if not ul:
        return []

    formats = []
    for item in ul.find_all("li"):
        texto = item.get_text(strip=True)
        if texto:
            formats.append(texto)
    return formats


def get_description(li_elem):
    # <div class='w-full'>
    div = li_elem.find("div", class_=lambda c: c and "markdown-content" in c)
    if not div:
        return ""
    p = div.find("p")
    if not p:
        return ""
    return next(
        (p.get_text(strip=True) for p in div.find_all("p") if p.get_text(strip=True)),
        ""
    )


def afficher_menus():
    print(f"{'=' * 100}")
    print(f"  {len(menus)} menus trouvés")
    print(f"{'=' * 100}\n")

    for i, menu in enumerate(menus, start=1):
        formats = ", ".join(f for f in menu.formats)
        print(f"{i:02d}. {menu.nom}")
        print(f"    URL        : {menu.url}")
        print(f"    Description: {menu.description}")
        print(f"    Formats    : {formats or 'Vide'}")
        print()


if __name__ == "__main__":
    main()
