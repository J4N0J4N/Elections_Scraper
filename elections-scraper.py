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


"""
cisla1 = [cislo.text.strip() for cislo in soup.find_all("td", headers="t1sa1 t1sb1")]  # Číslo1
cisla2 = [cislo.text.strip() for cislo in soup.find_all("td", headers="t2sa1 t2sb1")]  # Číslo2
cisla3 = [cislo.text.strip() for cislo in soup.find_all("td", headers="t3sa1 t3sb1")]  # Číslo3
nazvy1 = [nazev.text.strip() for nazev in soup.find_all("td", headers="t1sa1 t1sb2")]  # Název strany1
nazvy2 = [nazev.text.strip() for nazev in soup.find_all("td", headers="t2sa1 t2sb2")]  # Název strany2
nazvy3 = [nazev.text.strip() for nazev in soup.find_all("td", headers="t3sa1 t3sb2")]  # Název strany3
"""
cisla = []
nazvy = []

# Dynamicky vytvárame zoznamy pre cisla a nazvy
for i in range(1, 4):
    cisla += [cislo.text.strip() for cislo in soup.find_all("td", headers=f"t{i}sa1 t{i}sb1")]
    nazvy += [nazev.text.strip() for nazev in soup.find_all("td", headers=f"t{i}sa1 t{i}sb2")]

#print("Číslo:", cisla)
#print("Název:", nazvy)



rows = zip(cisla, nazvy)

header = ["Číslo", "Název", "Voliči v seznamu", "Odevzdané obálky", "Platné hlasy"]

with open("vysledky.csv", mode="w", encoding="UTF-8-sig") as nove_csv:
    zapisovac = csv.writer(nove_csv, delimiter=";")
    zapisovac.writerow(header)
    zapisovac.writerows(rows)


"""
# Function to fetch data from the given URL
def fetch_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching the URL: {response.status_code}")
        sys.exit(1)
    return bs(response.text, 'html.parser')

# Function to scrape election data
def scrape_election_data(url):
    soup = fetch_data(url)

    # Find all rows in the main table
    rows = soup.find_all("tr")[2:]  # Skip header rows

    # Data to store
    results = []

    for idx, row in enumerate(rows):
        columns = row.find_all("td")
        
        # Print out the row for debugging purposes
        print(f"Row {idx} columns: {len(columns)}")

        # Check if the row has enough columns
        if len(columns) < 5:
            print(f"Skipping row {idx}: Not enough columns")
            continue  # Skip rows with insufficient columns

        # Scrape the data
        location_code = columns[0].text.strip()
        location_name = columns[1].text.strip()
        voters = columns[2].text.strip()
        envelopes = columns[3].text.strip()
        valid_votes = columns[4].text.strip()

        # Collecting party results
        parties_votes = [col.text.strip() for col in columns[5:]]

        # Combine all into a single record
        result = [location_code, location_name, voters, envelopes, valid_votes] + parties_votes
        results.append(result)

    return results


# Function to save data into a CSV file
def save_to_csv(data, filename):
    headers = ["Location Code", "Location Name", "Voters", "Envelopes", "Valid Votes", "Party Results"]
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    print(f"Data saved to {filename}")

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python elections-scraper.py <url> <output_file.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    # Scrape election data and save to CSV
    election_data = scrape_election_data(url)
    save_to_csv(election_data, output_file)
"""