import os

import pandas as pd


def main():
    cat_dict = {}
    for file_name in os.listdir("csv"):
        if "_" in file_name:
            cat = file_name.split("_")[0]
            if cat not in cat_dict.keys():
                cat_dict[cat] = [file_name]
            else:
                cat_dict[cat].append(file_name)
        else:
            df_cur = pd.read_csv(os.path.join("csv", file_name))
            if "img_flag" in df_cur.columns:
                df_cur.drop("img_flag", axis=1, inplace=True)
            df_cur.to_csv(f"csv_full/{file_name.split('.')[0]}.csv", index=False)
    for k in cat_dict.keys():
        print(k, cat_dict[k])
        df = None
        for f in cat_dict[k]:
            df_cur = pd.read_csv(os.path.join("csv", f))
            df_cur.drop("img_flag", axis=1, inplace=True)
            if df is not None:
                df = pd.concat([df, df_cur]).drop_duplicates().reset_index(drop=True)
            else:
                df = df_cur.copy()
        print(df)
        df.to_csv(f"csv_full/{k}.csv", index=False)

if __name__ == "__main__":
    main()