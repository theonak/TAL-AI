from data import generate_urls, parse_url_team, shuffle_team, extract_one_champ
from tqdm import tqdm
import pandas as pd
urls = generate_urls(2021, 8, 1)
x_train = []
x_eval = parse_url_team(urls[0])

