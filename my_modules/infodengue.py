import pandas as pd

def url_factory(params):
  url = (
    "https://info.dengue.mat.br/api/alertcity?",
    "&disease=", params["dengue"],
    "&geocode=", params["geocode"],
    "&disease=", params["dengue"],
    "&format=", params["csv"],
    "&ew_start=", params["ew_start"],
    "&ew_end=", params["ew_end"],
    "&ey_start=", params["ey_start"],
    "&ey_end=", params["ey_end"]    
  )
  
  return "".join(map(str, url))

def get_dataset(params):
  url = url_factory(params)
  
  df = pd.read_csv(url, index_col='SE')

  df = df[["data_iniSE","casos"]]
  df.reset_index(drop=True, inplace=True)

  return df

def get_formated_dataset(params):
  df = get_dataset(params)
  
  df = df[["data_iniSE","casos"]]
  df.reset_index(drop=True, inplace=True)

  return df