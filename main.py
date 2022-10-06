from random import shuffle
from data import generate_urls, parse_url_match 
from tqdm import tqdm
import pandas as pd
import csv
urls = generate_urls(2022, 9, 1)

match_eval_df = pd.concat([parse_url_match(urls[i]) for i in range(30)])
match_train_df = pd.concat([parse_url_match(urls[i]) for i in range(30,len(urls))])

match_eval_df.to_csv("match_eval_df.csv")
match_train_df.to_csv("match_train_df.csv")

print(match_eval_df)
