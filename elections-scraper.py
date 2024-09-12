"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ján Jankovič
email: jankovic.jan4@gmail.com
discord: jano_15654 
"""
import requests
from bs4 import BeautifulSoup as bs
import csv
import sys

def fetch_soup(url):
    response = requests.get(url)
    return bs(response.text, 'html.parser')

def get_codes_and_names(soup):
    codes, names = [], []
    for i in range(1, 4):
        codes += [cislo.text.strip() for cislo in soup.find_all("td", headers=f"t{i}sa1 t{i}sb1")]
        names += [nazev.text.strip() for nazev in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2")]
    return codes, names

def get_hyperlinks(soup):
    hyperlinks = []
    for row in soup.find_all("tr"):
        link = row.find("a")
        if link:
            href = link['href']
            location_url = 'https://volby.cz/pls/ps2017nss/' + href
            hyperlinks.append(location_url)
    return hyperlinks

def get_votes_data(municipality_soup):
    registered = [voter.text.strip().replace("\xa0", " ") for voter in
                  municipality_soup.find_all("td", {"headers": "sa2"})]
    envelopes = [envelope.text.strip().replace("\xa0", " ") for envelope in
                 municipality_soup.find_all("td", {"headers": "sa3"})]
    valid = [valid_vote.text.strip().replace("\xa0", " ") for valid_vote in
             municipality_soup.find_all("td", {"headers": "sa6"})]

    partial_votes_per_link = []
    for i in range(1, 3):
        partial_votes_per_link += [vote.text.strip().replace("\xa0", " ") for vote in
                                   municipality_soup.find_all("td", headers=f"t{i}sa2 t{i}sb3") if
                                   vote.text.strip() != "-"]

    return registered, envelopes, valid, partial_votes_per_link

def get_parties(soup):
    parties = []
    for i in range(1, 3):
        parties += [party.text.strip() for party in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2") if
                    party.text.strip() != "-"]
    return parties

def write_to_csv(filename, header, parties, rows, partial_votes):
    with open(filename, mode="w", encoding="UTF-8-sig") as new_csv:
        writer = csv.writer(new_csv, delimiter=";")
        writer.writerow(header + parties)
        for row, votes in zip(rows, partial_votes):
            writer.writerow(list(row) + votes)


if __name__ == "__main__":
    try:
        # Skontroluj, či bol zadaný presne jeden argument (odkaz)
        url = sys.argv[1]
        csv_filename = sys.argv[2]

        if not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("Prvý argument nie je platná URL. Uistite sa, že začína 'http://' alebo 'https://'.")

        soup = fetch_soup(url)

    except IndexError:
        print("Chybí argument: Použitie: python skript.py <odkaz na stranku> <nazov csv suboru>")
        sys.exit(1)

    except requests.exceptions.MissingSchema:
        # Ak prvý argument nie je URL, zrejme boli argumenty v nesprávnom poradí
        print("Argumenty sú zadané v nesprávnom poradí. Prvý argument musí byť URL a druhý názov CSV súboru.")
        sys.exit(1)

    else:
        codes, names = get_codes_and_names(soup)
        hyperlinks = get_hyperlinks(soup)

        registered, envelopes, valid, partial_votes = [], [], [], []

        for municipality_url in hyperlinks:
            municipality_soup = fetch_soup(municipality_url)
            registered_voters, envelopes_issued, valid_votes, votes = get_votes_data(municipality_soup)
            registered += registered_voters
            envelopes += envelopes_issued
            valid += valid_votes
            partial_votes.append(votes)

        parties = get_parties(municipality_soup)
        rows = zip(codes, names, registered, envelopes, valid)
        header = ["Code", "Location", "Registered", "Envelopes", "Valid"]

        write_to_csv(csv_filename, header, parties, rows, partial_votes)


"""
#nakoniec to napíšem do jednej funkcie
url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=1&xnumnuts=1100"
response = requests.get(url)
soup = bs(response.text, features="html.parser")

#listy, kde sa ukladajú jednotlivé dáta na uloženie do csv
codes = []
names = []
parties = []
hyperlinks = []
registered = []
envelopes = []
valid = []
partial_votes = []

# cyklus dynamicky vytvára listy pre cisla a nazvy(range 1 - 4 kvoli tomu, ze tabulka je rozdelena na 3 rovnake tabulky)
for i in range(1, 4):
    codes += [cislo.text.strip() for cislo in soup.find_all("td", headers=f"t{i}sa1 t{i}sb1")]
    names += [nazev.text.strip() for nazev in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2")]

# cyklus, ktorý prechhádza jednotlivé riadky HTML, v tagu "a" nachádza element href(relatívna URL) a pripája k základnej URL + ukladá do listu hyperlinks
for row in soup.find_all("tr"):
    link = row.find("a")
    if link:
        href = link['href']
        location_url = 'https://volby.cz/pls/ps2017nss/' + href
        hyperlinks.append(location_url)  

# cyklus, ktorý prechádza cez všetky adresy v hyperlinks, sťahuje ich obsah, parsuje a ukladá do premennej municipality_soup
for municipality_url in hyperlinks:
    response = requests.get(municipality_url)
    municipality_soup = bs(response.text, 'html.parser')

    # cykly, ktoré priraduju do listov registered, envelopes a valid hodnoty z jednotlivych hyperlinkov
    registered += [registered_voters.text.strip().replace("\xa0", " ") for registered_voters in municipality_soup.find_all("td", {"headers": "sa2"})]
    envelopes += [issued_envelopes.text.strip().replace("\xa0", " ") for issued_envelopes in municipality_soup.find_all("td", {"headers": "sa3"})]
    valid += [valid_votes.text.strip().replace("\xa0", " ") for valid_votes in municipality_soup.find_all("td", {"headers": "sa6"})]

    # list, do ktorého sa ukladajú hlasy pre jednotlivé strany postupne podľa obce
    partial_votes_per_link = []
    # cylkus, ktorý scrapuje počty hlasov pre jednotlivé strany podľa obce
    for i in range(1, 3):
        partial_votes_per_link += [cislo.text.strip().replace("\xa0", " ") for cislo in municipality_soup.find_all("td", headers=f"t{i}sa2 t{i}sb3") if cislo.text.strip() != "-"]
    partial_votes.append(partial_votes_per_link)

# cyklus dynamicky vytvára list pre politické strany(range 1 - 3 kvoli tomu, ze tabulka je rozdelena na 2 rovnake tabulky)
for i in range(1, 3):
    parties += [party.text.strip() for party in municipality_soup.find_all("td", headers=f"t{i}sa1 t{i}sb2") if party.text.strip() != "-"]


# v premennej rows su ulozene jednotlive kombinacie kodov a nazvov obci do dvojic
rows = zip(codes, names, registered, envelopes, valid)

# nemenna hlavicka csv
header = ["Code", "Location", "Registered", "Envelopes", "Valid"]

# zapis hlavicky spolu s vyscapovanymi nazvami stran do prveho riadku
# zapis jednotlivych údajov z premennej rows do prvych piatich stlpcov
# kombinácia a spojenie rows s hlasmi pre politické strany a zápis po jednotlivých riadkoch
with open("vysledky.csv", mode="w", encoding="UTF-8-sig") as new_csv:
    writer = csv.writer(new_csv, delimiter=";")
    writer.writerow(header+ parties)
    for row, votes in zip(rows, partial_votes):
        writer.writerow(list(row) + votes)
"""