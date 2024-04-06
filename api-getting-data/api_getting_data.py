import requests
import csv

url = 'https://api.chucknorris.io/jokes/random'
response = requests.get(url)

if response.status_code == 200:
    joke_data = response.json()['value']

    csv_file_path = 'chuck_norris_joke.csv'

    field_names = ['Joke']

    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)

        writer.writeheader()

        writer.writerow({'Joke': joke_data})

    print("Data successfully saved to", csv_file_path)
else:
    print("Error:", response.status_code)
