from data import generate_urls, parse_url_team, shuffle_team, extract_one_champ
from tqdm import tqdm
import pandas as pd
urls = generate_urls(2021, 8, 1)
x_train = []
x_eval = parse_url_team(urls[0])

shuffle_team(x_eval)
eval_team, eval_champ = extract_one_champ(x_eval)

eval_team_df = pd.DataFrame(eval_team)
eval_champ_df = pd.DataFrame(eval_champ)

eval_team_df.to_csv("datasets/eval_team_df.cvs")
eval_champ_df.to_csv("datasets/eval_champ_df.csv")
