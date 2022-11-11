import os

import pandas as pd
from cinemagoer.imdb import Cinemagoer
import requests
from bs4 import BeautifulSoup as bs
import re

from genre_parser import get_info


def main(films_amount = 300, type_search = "genres", genres = []):
    # start parsing by genres
    for genre in genres:
        film_id_dict = {}
        data_films = []
        ia = Cinemagoer()
        for start in [1 + i * 50 for i in range(films_amount//50)]:
            if start != 1:
                response = requests.get(f"https://www.imdb.com/search/title/?{type_search}={genre.lower()}&start={start}").content
            else:
                response = requests.get(f"https://www.imdb.com/search/title/?{type_search}={genre.lower()}").content
            soup = bs(response, 'html.parser')

            for l in soup.find_all('a'):
                if "title/tt" in str(l):
                    id = re.search(f"title/tt(.*)/", str(l)).group(1).split("/")[0]
                    id = "".join([i for i in id if i.isdigit()])
                    if id not in film_id_dict.keys():
                        film_id_dict[id] = 0
        print(film_id_dict.keys())
        print(len(film_id_dict.keys()))
        i = 0
        for film_id in film_id_dict.keys():
            i += 1
            print(f"({i}/{len(film_id_dict.keys())}) {film_id}")
            data_films.append(get_info(ia, film_id, genre))
        df = pd.DataFrame(data_films,
                          columns=["movie_id", "original_title", "genres", "synopsis", "cover_url", "orig_genre"])
        os.makedirs("csv", exist_ok=True)
        df.to_csv(f"csv/{genre.lower()}.csv", index=False)

if __name__ == "__main__":
    main(300, "genres", ["documentary", "Short"])
    main(300, "keywords", ["Superhero"])
