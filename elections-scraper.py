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

def get_soup(url):
    """Funkcia získava HTML obsah z web stránky a parsuje ho."""
    response = requests.get(url)
    return bs(response.text, 'html.parser')

def get_codes_and_names(soup):
    """
    Funkcia vyhľadáva pomocou cyklu kódy a názvy obcí v 3 tabuľkách(range 1, 4) na danom odkaze a
    vracia ich ako listy codes a names.
    """
    codes, names = [], []
    for i in range(1, 4):
        codes += [cislo.text.strip() for cislo in soup.find_all("td", headers=f"t{i}sa1 t{i}sb1")]
        names += [nazev.text.strip() for nazev in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2")]
    return codes, names

def get_hyperlinks(soup):
    """
    Funkcia, ktorá pomocou cyklu prechhádza jednotlivé riadky HTML, v tagu "a" nachádza element 
    href(relatívna URL) a pripája k základnej URL + ukladá do listu hyperlinks, ktorý vracia.
    """
    hyperlinks = []
    for row in soup.find_all("tr"):
        link = row.find("a")
        if link:
            href = link['href']
            location_url = 'https://volby.cz/pls/ps2017nss/' + href
            hyperlinks.append(location_url)
    return hyperlinks

def get_votes_data(municipality_soup):
    """
    Funkcia pozostáva z 3 cyklov, ktoré priraďujú premenným registered, envelopes a valid hodnoty z 
    jednotlivych hyperlinkov. Funkcia obsahuje ešte jeden cyklus, ktorý scrapuje počty hlasov pre 
    jednotlivé strany podľa obce. Nakoniec funkcia vracia 4 listy.
    """
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
    """
    Funkcia využíva cyklus, ktorý dynamicky vytvára list pre názvy politických strán. Tento zoznam
    je použitý pri vytváraní hlavičky CSV súboru.
    """
    parties = []
    for i in range(1, 3):
        parties += [party.text.strip() for party in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2") if
                    party.text.strip() != "-"]
    return parties

def write_to_csv(filename, header, parties, rows, partial_votes):
    """
    Funkcia zapisuje vyscrapované dáta do CSV súboru. Zapisuje hlavičku(header), ktorá je fixne
    zadefinovaná do jedného riadku s názvami politických strán. Následne zapisuje pomocou cyklu
    po riadkoch dáta uložené do listov(codes, names...) spolu s počtom hlasov, ktoré jednotlivé
    strany získali v danej obci.
    """
    with open(filename, mode="w", encoding="UTF-8-sig") as new_csv:
        writer = csv.writer(new_csv, delimiter=";")
        writer.writerow(header + parties)
        for row, votes in zip(rows, partial_votes):
            writer.writerow(list(row) + votes)

def process_input():
    """Funkcia spracuje vstupy z príkazového riadku, očakáva 2 argumenty"""
    try:
        url = sys.argv[1]
        csv_filename = sys.argv[2]
    except IndexError:
        print("Nesprávne zadané argumenty. Použitie: python skript.py <odkaz_na_stránku> <názov_csv_súboru>")
        sys.exit(1)
    return url, csv_filename

def scrape_data(url):
    """
    Funkcia získa kódy, názvy obcí. Následne zavolá funkciu get_hyperlinks a získa odkazy na detaily o
    jednotlivých obciach. Pomocou cyklu funkcia vyscrapuje dáta o voličoch, vydaných obálkach, platných
    hlasoch a hlasoch pre jednotlivé plitické strany rozdelené podľa obcí zavolaním funkcie get_votes_data
    a vráti ich ako listy.
    """
    soup = get_soup(url)
    codes, names = get_codes_and_names(soup)
    hyperlinks = get_hyperlinks(soup)
    registered, envelopes, valid, partial_votes = [], [], [], []

    # Cyklus na scrapovanie dát z jednotlivých odkazov
    for municipality_url in hyperlinks:
        municipality_soup = get_soup(municipality_url)
        registered_voters, envelopes_issued, valid_votes, votes = get_votes_data(municipality_soup)
        registered += registered_voters
        envelopes += envelopes_issued
        valid += valid_votes
        partial_votes.append(votes)
    return codes, names, registered, envelopes, valid, partial_votes, hyperlinks

def main():
    """
    Hlavná funkcia, ktorá spája celý proces. Zavolá funkciu process_input, ktorá overí vstupy od užívateľa.
    Následne je zavolaná funkcia scrape_data, ktorá získa všetky potrebné údaje a uloží ich do premenných.
    Zavolaním funkcie get_parties sú vyscrapované názvy politických subjektov z posledného hyperlinku.
    Všetky dáta sú nakoniec zapísané do CSV súboru.
    """
    url, csv_filename = process_input()
    try:
        soup = get_soup(url)
        print(f"STAHUJEM DATA Z VYBRANEHO URL: {url}")

        codes, names, registered, envelopes, valid, partial_votes, hyperlinks = scrape_data(url)
        parties = get_parties(get_soup(hyperlinks[-1]))
        rows = zip(codes, names, registered, envelopes, valid)
        header = ["Code", "Location", "Registered", "Envelopes", "Valid"]
        write_to_csv(csv_filename, header, parties, rows, partial_votes)
        print(f"UKLADAM DO SUBORU: {csv_filename}\nUKONCUJEM elections-scraper")
    except requests.exceptions.MissingSchema:
        print("Argumenty sú zadané v nesprávnom poradí. Prvý argument musí byť URL a druhý názov CSV súboru.\n"
              "Použitie: python skript.py <odkaz_na_stránku> <názov_csv_súboru>")
        sys.exit(1)

if __name__ == "__main__":
    main()
