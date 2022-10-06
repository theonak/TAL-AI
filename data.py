from numpy import dtype
from champs import champ_to_one_hot
import pandas as pd
from tqdm import tqdm
from random import shuffle
import tensorflow as tf
from champs import NB_CHAMP


def parse_url_match(url) :
    df = pd.read_html(url, header=1)[0]
    df = pd.concat([df["P"],df["Blue"],df["Red"],df["Winner"],df["Bans"],df["Bans.1"],df["Picks"],df["Picks.1"]],axis=1)
    df = df.drop(0)
    df["Blue wins"] = (df["Blue"]==df["Winner"])
    out = pd.concat([df["Bans"],df["Bans.1"],df["Picks"],df["Picks.1"]],axis=1)
    out["Blue wins"] = df["Blue wins"]
    
    out["Bans"] = [[champ_to_one_hot(champ) for champ in element.split(",")] for element in df["Bans"]]
    out["Bans.1"] = [[champ_to_one_hot(champ) for champ in element.split(",")] for element in df["Bans.1"]]
    out["Picks.1"] = [[champ_to_one_hot(champ) for champ in element.split(",")] for element in df["Picks.1"]]
    out["Picks"] = [[champ_to_one_hot(champ) for champ in element.split(",")] for element in df["Picks"]]
    
    return out

def parse_url_team(url) :
    df = parse_url_match(url)
    df = pd.concat([df["Picks"],df["Picks.1"]],axis=1)
    return df



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
  while year != 2022 or month != 10 or day != 6 :
    y, m, d = next_date(year, month, day)
    urls.append(start_url + date_str(year, month, day) + mid_url + date_str(y, m, d) + end_url)
    year, month, day = y, m, d
  return urls


def shuffle_df(data) :
  for key in data.keys() :
    for x in data[key] :
      shuffle(x)


def extract_one_champ(dataframe) :
    team = tf.convert_to_tensor([x[:4] for x in dataframe.values])
    champ = tf.convert_to_tensor([x[4] for x in dataframe.values])
    return team, champ

def load(name) :
    """
    # Input
        name : "champ_df", "eval_champ_df", "team_df", "eval_team_df"  
    """
    return pd.read_csv("datasets/"+name)
  
def format(dataframe) :
    for column in ["Picks","Picks.1","Bans","Bans.1"] :
      for i in range(len(dataframe[column])) :
        x = dataframe[column].values[i]
        x = x.replace("[","")
        x = x.replace("]","")
        x = x.split(",")
        x = [[boolean==' 1' for boolean in x[i*NB_CHAMP:(i+1)*NB_CHAMP]] for i in range(5)]
        dataframe[column].values[i] = x
