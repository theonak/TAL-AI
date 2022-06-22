from random import shuffle
from data import generate_urls, parse_url_team, shuffle_team, extract_one_champ, parse_url_match 
from tqdm import tqdm
import pandas as pd
urls = generate_urls(2021, 8, 1)

x_eval, y_eval = parse_url_match(urls[0])
train_ds = [parse_url_match(urls[i]) for i in range(1,len(urls))]
x_train = []
y_train = []
for game in train_ds :
    x, y = game
    x_train.append(x)
    y_train.append(y)



match_eval_df = pd.DataFrame(x_eval)
result_eval_df = pd.DataFrame(y_eval)
match_train_df = pd.DataFrame(x_train)
result_train_df = pd.DataFrame(y_train)

match_eval_df.to_csv("match_eval_df.csv")
result_eval_df.to_csv("result_eval_df.csv")
match_train_df.to_csv("match_train_df.csv")
result_train_df.to_csv("result_train_df.csv")

