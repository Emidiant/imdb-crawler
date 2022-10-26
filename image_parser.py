import os
import time

import pandas as pd
import requests

def main():
    time_out = 0
    df_list = []
    while time_out < 1200:
        Bset = frozenset(df_list)
        new_files = [item for item in os.listdir("csv") if item not in Bset]
        if new_files:
            print(f"New files: {new_files}")
        df_list = os.listdir("csv")
        processed_file = 0
        for file_name in new_files:
            df = pd.read_csv(os.path.join("csv", file_name), dtype={'movie_id': str})
            if "img_flag" not in df.columns:
                df["img_flag"] = False

            id_img_dict = dict(zip(df.movie_id, df.img_flag))
            i = 0
            if False not in df.img_flag.values:
                continue

            print(file_name)
            processed_file += 1
            try:
                for film_info in df.iterrows():
                    i += 1
                    print(f"({i}/{df.shape[0]}) {film_info[1].movie_id}, {film_info[1].original_title}")
                    if not film_info[1].img_flag:
                        try:
                            img_data = requests.get(film_info[1].cover_url).content
                            os.makedirs(os.path.join("images", film_info[1].orig_genre.lower()), exist_ok=True)
                            with open(os.path.join("images", film_info[1].orig_genre.lower(), f"{film_info[1].orig_genre.lower()}_{film_info[1].movie_id}.jpg"), 'wb') as img_handler:
                                img_handler.write(img_data)
                            id_img_dict[film_info[1].movie_id] = True
                        except Exception as e:
                            print(e)
            except KeyboardInterrupt as e:
                df["img_flag"] = df["movie_id"].apply(lambda x: id_img_dict[x])
                return 0

            df["img_flag"] = df["movie_id"].apply(lambda x: id_img_dict[x])
            df[df["img_flag"] != False].to_csv(os.path.join("csv", file_name), index=False)
        if processed_file == 0:
            time_out += 30
        else:
            time_out = 0
        print(f"Processed files: {processed_file}, timeout: {time_out}")
        time.sleep(30)

if __name__ == "__main__":
    main()
