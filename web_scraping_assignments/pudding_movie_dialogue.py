import csv
import requests
from bs4 import BeautifulSoup

def scrape_movie_dialogue(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        dialogue = soup.get_text()[:1000]  # Get the first 1000 characters of dialogue
        return dialogue
    except Exception as e:
        print(f"Error scraping dialogue from {url}: {e}")
        return None

with open('cleaned_pudding_data.csv', 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    with open('pudding_movie_dialogue.csv', 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['URL', 'Dialogue'])  # Write header row
        for row in reader:
            url = row[0]  # Assuming the URL is in the first column of the CSV
            dialogue = scrape_movie_dialogue(url)
            writer.writerow([url, dialogue])
