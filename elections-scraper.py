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


url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101"

response = requests.get(url)

soup = bs(response.text, features="html.parser")



cisla = []
nazvy = []
strany = []


# Dynamicky vytvárame zoznamy pre cisla a nazvy
for i in range(1, 4):
    cisla += [cislo.text.strip() for cislo in soup.find_all("td", headers=f"t{i}sa1 t{i}sb1")]
    nazvy += [nazev.text.strip() for nazev in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2")]

riadky = soup.find_all("tr")

hyperlinky = []

for riadok in riadky:
    link = riadok.find("a")
    if link:
        href = link['href']
        obec_url = 'https://volby.cz/pls/ps2017nss/' + href
        hyperlinky.append(obec_url)
        


for obec_url in hyperlinky:
    response = requests.get(obec_url)
    obec_soup = bs(response.text, 'html.parser')

strany += [strana.text.strip() for strana in obec_soup.find_all("td", headers="t1sa1 t1sb2")]
strany += [strana.text.strip() for strana in obec_soup.find_all("td", headers="t2sa1 t2sb2")]

rows = zip(cisla, nazvy)

header = ["Číslo", "Název", "Voliči v seznamu", "Odevzdané obálky", "Platné hlasy"]

with open("vysledky.csv", mode="w", encoding="UTF-8-sig") as nove_csv:
    zapisovac = csv.writer(nove_csv, delimiter=";")
    zapisovac.writerow(header + strany)
    zapisovac.writerows(rows)

