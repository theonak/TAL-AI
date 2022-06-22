from champs import champ_to_one_hot
import pandas as pd
from tqdm import tqdm
from random import shuffle

def parse_url_match(url) :
    df = pd.read_html(url, header=1)[0]
    df = pd.concat([df["P"],df["Blue"],df["Red"],df["Winner"],df["Bans"],df["Bans.1"],df["Picks"],df["Picks.1"]],axis=1)
    df = df.drop(0)
    df["Blue wins"] = (df["Blue"]==df["Winner"])
    df = pd.concat([df["P"],df["Blue wins"],df["Bans"],df["Bans.1"],df["Picks"],df["Picks.1"]],axis=1)

    bans_list = []
    for element in df["Bans"] :
        bans_list.append([champ_to_one_hot(champ) for champ in element.split(",")])
    df["Bans"] = bans_list

    bans1_list = []
    for element in df["Bans.1"] :
        bans1_list.append([champ_to_one_hot(champ) for champ in element.split(",")])
    df["Bans.1"] = bans1_list

    Picks_list = []
    for element in df["Picks"] :
        Picks_list.append([champ_to_one_hot(champ) for champ in element.split(",")])
    df["Picks"] = Picks_list

    Picks1_list = []
    for element in df["Picks.1"] :
        Picks1_list.append([champ_to_one_hot(champ) for champ in element.split(",")])
    df["Picks.1"] = Picks1_list
    X_training = []
    Y_training = pd.DataFrame(df["Blue wins"]).values
    for i in range(len(Y_training)) :
        X_vector = []
        X_vector.extend(df["Bans"][i+1])
        X_vector.extend(df["Bans.1"][i+1])
        X_vector.extend(df["Picks"][i+1])
        X_vector.extend(df["Picks.1"][i+1])
        X_training.append(X_vector)
    return X_training, Y_training

def parse_url_team(url) :
    df = pd.read_html(url, header=1)[0]
    df = df.drop(0)
    df = pd.concat([df["Picks"],df["Picks.1"]],axis=1)


    Picks_list = []
    for element in df["Picks"] :
        Picks_list.append([champ_to_one_hot(champ) for champ in element.split(",")])
    df["Picks"] = Picks_list

    Picks1_list = []
    for element in df["Picks.1"] :
        Picks1_list.append([champ_to_one_hot(champ) for champ in element.split(",")])
    df["Picks.1"] = Picks1_list
    X_training = []
    n = len(df["Picks"])
    for i in range(n) :
        X_training.append(df["Picks"][i+1])
        X_training.append(df["Picks.1"][i+1])
    return X_training

start_url = "https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D=&MHG%5Bteam%5D=&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=200&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D="
mid_url = "&MHG%5Benddate%5D="
end_url = "&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="

daymax = 28
monthmax = 12

def date_str(year, month, day):
  return str(year) + "-" + str(month) + "-" + str(day)

def next_date(year, month, day):
  day += 1
  if day>daymax:
    day = 1
    month+=1
  if month>monthmax:
    month=1
    year+=1
  return year, month, day

def generate_urls(start_year, start_month, start_day):
  urls = []
  day = start_day
  month = start_month
  year = start_year
  while year != 2022 or month != 6 or day != 21 :
    y, m, d = next_date(year, month, day)
    urls.append(start_url + date_str(year, month, day) + mid_url + date_str(y, m, d) + end_url)
    year, month, day = y, m, d
  return urls


def shuffle_team(data, nb_shuffle=10) : 
    for _ in tqdm(range(nb_shuffle)) :
        for x in data :
            shuffle(x)

def extract_one_champ(data) :
    team = [x[:4] for x in data]
    champ = [x[4] for x in data]
    return team, champ

def load(name) :
    """
    # Input
        name : "champ_df", "eval_champ_df", "team_df", "eval_team_df"  
    """
    return pd.read_csv("datasets/"+name)