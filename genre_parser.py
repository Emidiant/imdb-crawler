import os

import pandas as pd
from imdb import Cinemagoer


def get_info(ia, movie_id, genre):
    film = ia.get_movie(movie_id)
    if "plot" in film.keys():
        synopsis = film["plot"][0]
    else:
        synopsis = ""
    cover_url = film.get_fullsizeURL()

    if "original title" not in film.keys():
        if "title" in film.keys():
            title = film["title"]
        else:
            title = film['canonical title']
    else:
        title = film["original title"]

    print(title, film["genres"])
    return movie_id, title, film["genres"], synopsis, cover_url, genre

def main():
    categories = """
    1. Action
    2. Adventure
    3. Animation
    4. Biography
    5. Comedy
    6. Crime
    8. Drama
    9. Family
    10. Fantasy
    11. Film-Noir
    12. History
    13. Horror
    14. Music
    15. Musical
    16. Mystery
    17. Romance
    18. Sci-Fi
    20. Sport
    21. Superhero
    22. Thriller
    23. War
    24. Western
    """
    # Documentary and short in separate script
    categories_list = [f.split(". ")[-1].strip() for f in categories.split("\n") if ". " in f]
    os.makedirs("csv", exist_ok=True)
    file_name_list = os.listdir("csv")
    # выбирается по 50 фильмов
    start_list = [0, 51, 101, 151, 201, 251]
    for start in start_list:
        j = 0
        for cat in categories_list:
            j += 1
            if f"{cat.lower()}_{start}.csv" in file_name_list:
                continue
            data_films = []
            print(f"Category: {cat}, start from {start}")
            i = 0
            ia = Cinemagoer()
            film_cat = ia.get_top50_movies_by_genres(cat, start)
            for mov in film_cat:
                i += 1
                print(f"({i}/{50}) {cat} ({j}/{len(categories_list)}), {start}-{start+50}, {mov.movieID}")
                movie_id, title, genres, synopsis, cover_url, genre = get_info(ia, mov.movieID, cat)
                if synopsis != "":
                    data_films.append([movie_id, title, genres, synopsis, cover_url, genre])
            df = pd.DataFrame(data_films, columns=["movie_id", "original_title", "genres", "synopsis", "cover_url", "orig_genre"])
            df.to_csv(f"csv/{cat.lower()}_{start}.csv", index=False)


if __name__ == "__main__":
    main()
