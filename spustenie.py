import requests
from bs4 import BeautifulSoup as bs
import sys

def get_url(link):
    if not link:
        return None
    
    return f"Stahuji data z vybraneho url: {link}"


def get_soup(url):
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    return(soup)
#print(get_soup("https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"))


if __name__ == "__main__":
    try:
        # Skontroluj, či bol zadaný presne jeden argument (odkaz)
        odkaz = sys.argv[1]
    except IndexError:
        print("Chybí argument: Použitie: python skript.py <odkaz na stranku>")
    else:
        print(get_url(odkaz))

        # Pokúsi sa získať obsah stránky
        soup = get_soup(odkaz)

        if soup:
            # Ak bol obsah úspešne získaný, zobrazí prvých 200 znakov
            html_content = soup.prettify()
            print(html_content[:200])
        else:
            print("Nepodarilo sa získať alebo spracovať HTML obsah.")