import pandas as pd

def url_factory(params):
  url = (
    "https://info.dengue.mat.br/api/alertcity?",
    "&disease=", "dengue",
    "&geocode=", params["geocode"],
    "&disease=", "dengue",
    "&format=", "csv",
    "&ew_start=", "1",
    "&ew_end=", "53",
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
  
  df["data_iniSE"] = pd.to_datetime(df["data_iniSE"])
  df["year"] = df["data_iniSE"].dt.year
  df["month"] = df["data_iniSE"].dt.month

  return df

def get_city_data(df_city, start, end):
  df_city["data_iniSE"] = pd.to_datetime(df_city["data_iniSE"])
  start = pd.to_datetime(start)
  end = pd.to_datetime(end)
  
  return df_city[ (df_city["data_iniSE"] >= start) & (df_city["data_iniSE"] <= end) ]