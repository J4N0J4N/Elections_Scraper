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

#def get_soup(url: str):
#    return bs(requests.get(url).text, features="html.parser")


url = "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=506761&xvyber=7103"

response = requests.get(url)

soup = bs(response.text, features="html.parser")

volici = soup.find("td", headers="sa2").text.strip()
odevzdane_obalky = soup.find("td", headers="sa3").text.strip()
platne_hlasy = soup.find("td", headers="sa6").text.strip()

strany = []

for strana in url:
    strany.append(soup.find("td", class_="overflow_name"))

#("a", {"class": "topic"})

print(strany)

elementy = [volici, odevzdane_obalky, platne_hlasy]



header = ["Voliči v seznamu", "Odevzdané obálky", "Platné hlasy"]

with open("prvni_tabulkovy_soubor.csv", mode="w", encoding="UTF-8-sig") as nove_csv:
    zapisovac = csv.writer(nove_csv, delimiter=";")
    zapisovac.writerows(
        (
            header,
            elementy
        )
    )

#<td class="cislo" headers="sa2" data-rel="L1">205</td>

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
    rows = soup.find_all("tr")[2:]  # Adjust indexing based on the table structure

    # Data to store
    results = []

    for row in rows:
        columns = row.find_all("td")
        
        # Check if the row has the expected number of columns (at least 5)
        if len(columns) >= 5:
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
        else:
            print(f"Skipping row with insufficient columns: {columns}")
            
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
        print("Usage: python election-scraper.py <url> <output_file.csv>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]

    # Scrape election data and save to CSV
    election_data = scrape_election_data(url)
    save_to_csv(election_data, output_file)
"""