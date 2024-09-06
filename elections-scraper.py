"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Ján Jankovič
email: jankovic.jan4@gmail.com
discord: jano_15654 
"""
import requests
from bs4 import BeautifulSoup as bs


def get_url(url: str):
    return bs(requests.get(url).text, features="html.parser")

rozdelene_html = get_url("https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103")

element = rozdelene_html.select("#ps311_t1 > tbody > tr:nth-child(3) > td:nth-child(5)")
if element:
    print("Element found:", element)
else:
    print("Element not found")
