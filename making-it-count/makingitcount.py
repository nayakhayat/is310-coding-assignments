import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
# subset to relevant urls
humanist_urls = ["https://humanist.kdl.kcl.ac.uk/Archives/Converted_Text/", "https://humanist.kdl.kcl.ac.uk/Archives/Current/"]
volume_dfs = []
# loop through each url
for url in humanist_urls:
    print(f"Getting volumes from {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a')
    # loop through each volume link
    for link in links:
        if link['href'].endswith('.txt'):
            print(f"Getting volume from {url + link['href']}")
            page_soup = BeautifulSoup(requests.get(url + link['href']).text, "html.parser")
            text = page_soup.get_text()
            volume_link = url + link['href']
            dates = link['href'].split('.')[1]
            data_dict = {'volume_text': text, 'volume_link': volume_link, 'volume_dates': dates}
            volume_dfs.append(data_dict)

scraped_humanist_df = pd.DataFrame(volume_dfs)
# Extract the volume number from the dates
scraped_humanist_df['volume_number'] = scraped_humanist_df['volume_dates'].str.extract(r'(\d+)')
# Remove numbers with more than 2 digits
scraped_humanist_df['volume_number'] = scraped_humanist_df['volume_number'].apply(lambda x: np.nan if len(str(x)) > 2 else x)

# Replace nulls with a sequential of volume numbers
scraped_humanist_df['volume_number'] = scraped_humanist_df['volume_number'].fillna(pd.Series(np.arange(1, len(scraped_humanist_df) + 1)))

# Extract the start and end years
scraped_humanist_df[['inferred_start_year', 'inferred_end_year']] = scraped_humanist_df['volume_dates'].str.split('-', expand=True)

# Remove years that are not 4 digits
scraped_humanist_df.inferred_start_year = scraped_humanist_df.inferred_start_year.apply(lambda x: np.nan if len(str(x)) != 4 else x)
scraped_humanist_df.inferred_end_year = scraped_humanist_df.inferred_end_year.apply(lambda x: np.nan if len(str(x)) != 4 else x)

# Ensure the years are numeric
scraped_humanist_df.loc[scraped_humanist_df.inferred_end_year.isnull(), 'inferred_end_year'] = np.nan

# Create an empty dummy variable for the years
start_year_before = None
end_year_before = None

# Loop through dataframe row by row
for index, row in scraped_humanist_df.iterrows():
    # Check that both start and end years are not null
    if (not pd.isnull(row.inferred_start_year)) and (not pd.isnull(row.inferred_end_year)):
        # assign the years to the dummy variables
        start_year_before = row.inferred_start_year
        end_year_before = row.inferred_end_year
        # print the years
        print(start_year_before, end_year_before)
    # Check that if years are null and the dummy variables are not, then update the years in the dataframe
    elif (pd.isnull(row.inferred_start_year) and start_year_before is not None) and (pd.isnull(row.inferred_end_year) and end_year_before is not None):
        # increment the years by 1
        start_year_before = int(start_year_before) + 1
        end_year_before = int(end_year_before) + 1
        # assign the years to the dataframe using the row index to update the original dataframe
        scraped_humanist_df.at[index, 'inferred_start_year'] = start_year_before
        scraped_humanist_df.at[index, 'inferred_end_year'] = end_year_before
        print(start_year_before, end_year_before)

# Save the dataframe to a csv
scraped_humanist_df.to_csv("web_scraped_humanist_listserv_volumes.csv", index=False)