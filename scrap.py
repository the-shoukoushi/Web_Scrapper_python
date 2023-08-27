
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

url = 'https://www.imdb.com/search/title/?title_type=feature&release_date=2021-01-01,2021-12-31&title_type=feature'
response = requests.get(url)

# Parsing the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Scraping the rankings section
rank_data_html = soup.select('.text-primary')
rank_data = [rank.text for rank in rank_data_html]
rank_data = list(map(float, rank_data))
print(rank_data[:6])

# Scraping the title section
title_data_html = soup.select('.lister-item-header a')
title_data = [title.text for title in title_data_html]
print(title_data[:6])

# Scraping the description section
description_data_html = soup.select('.ratings-bar+ .text-muted')
description_data = [re.sub(r'\n', '', desc.text) for desc in description_data_html]
print(description_data[:6])

# Scraping the Movie runtime section
runtime_data_html = soup.select('.text-muted .runtime')
runtime_data = [re.sub(r' min', '', runtime.text) for runtime in runtime_data_html]
runtime_data = list(map(int, runtime_data))
print(runtime_data[:6])

# Scraping the Movie genre section
genre_data_html = soup.select('.genre')
genre_data = [re.sub(r'\n', '', genre.text) for genre in genre_data_html]
genre_data = [genre.strip() for genre in genre_data]
genre_data = [genre.split(',')[0] for genre in genre_data]
genre_data = pd.Series(genre_data, dtype='category')
print(genre_data[:6])

# Scraping the IMDB rating section
rating_data_html = soup.select('.ratings-imdb-rating strong')
rating_data = [float(rating.text) for rating in rating_data_html]
print(rating_data[:6])

# Scraping the votes section
votes_data_html = soup.select('.sort-num_votes-visible span:nth-child(2)')
votes_data = [re.sub(r',', '', votes.text) for votes in votes_data_html]
votes_data = list(map(int, votes_data))
print(votes_data[:6])

# Scraping the directors section
directors_data_html = soup.select('.text-muted+ p a:nth-child(1)')
directors_data = [director.text for director in directors_data_html]
directors_data = pd.Series(directors_data, dtype='category')
print(directors_data[:6])

# Scraping the actors section
actors_data_html = soup.select('.lister-item-content .ghost+ a')
actors_data = [actor.text for actor in actors_data_html]
actors_data = pd.Series(actors_data, dtype='category')
print(actors_data[:6])

# Combining all the lists to form a data frame
movies_df = pd.DataFrame({
    'Rank': rank_data,
    'Title': title_data,
    'Description': description_data,
    'Runtime': runtime_data,
    'Genre': genre_data,
    'Rating': rating_data,
    'Votes': votes_data,
    'Director': directors_data,
    'Actor': actors_data
})

# Structure of the data frame
print(movies_df.info())
print(movies_df.head())

# Saving the DataFrame to CSV
movies_df.to_csv('movies_data.csv', index=False)

print("CSV file 'movies_data.csv' has been saved successfully.")
