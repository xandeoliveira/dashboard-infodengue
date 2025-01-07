import pandas as pd
import numpy as np
import os

def request_city_info(geocode, ws, we, ys, ye):
  URL = "https://info.dengue.mat.br/api/alertcity"
  params = (
    "&disease=dengue&geocode=" + f"{geocode}"
    + "&disease=dengue&format=csv"
    + "&ew_start=" + f"{ws}" + "&ew_end=" + f"{we}"
    + "&ey_start=" + f"{ys}" + "&ey_end=" + f"{ye}"
  )

  url_resp = "?".join([URL, params])
  info = pd.read_csv(url_resp, index_col='SE')

  return info

def get_city_info(city, interval):
  code = {
    "Acarape": 2300150,
    "Redenção": 2311603
  }
  ws, ys, we, ye = interval

  city_info = request_city_info(code[city], ws, we, ys, ye)
  city_info.drop(columns=['casos_est','casos_est_min','casos_est_max',
                          'Localidade_id','id','versao_modelo','tweet',
                          'casprov','casprov_est','casprov_est_min',
                          'casprov_est_max','casconf'], inplace=True)
  return city_info

def get_main_indexes(df):
  # data_iniSE no formato YYYY-MM-DD, convertendo para MM-YYYY
  df = df[['data_iniSE']]
  dates = list()

  for date in df.loc[:, 'data_iniSE']:
    dates.append(date[:7])

  df.loc[:, 'data_iniSE'] = dates

  return dates

def get_monthly_cases(df, main_indexes, unique_indexes):
  # Somando os casos para um mesmo mês
  df = df[['data_iniSE','casos']]
  month_cases = list()

  for month in unique_indexes:
    weeks = df[df['data_iniSE'] == month]
    month_cases.append(weeks['casos'].sum())

  return month_cases

def get_monthly_dataframe(data_array):
  # Criando o DataFrame com o formato desejado
  df_monthly_cases = pd.DataFrame(data=data_array)
  df_monthly_cases.set_index('Index', inplace=True)
  df_monthly_cases.index.name = None

  return df_monthly_cases

# def get_monthly_temp(df, main_indexes, unique_indexes):
#     # Somando os casos para um mesmo mês
#   df = df[['data_iniSE','tempmin','tempmed','tempmax']]
#   tempmin = list()
#   tempmed = list()
#   tempmax = list()

#   for month in unique_indexes:
#     weeks = df[df['data_iniSE'] == month]
#     tempmin.append(weeks['tempmin'].sum() / len(weeks['tempmin']))
#     tempmed.append(weeks['tempmed'].sum() / len(weeks['tempmed']))
#     tempmax.append(weeks['tempmax'].sum() / len(weeks['tempmax']))

#   return tempmin, tempmed, tempmax

interval = (1, 2024, 53, 2024)
city = "Acarape"

df_main = get_city_info(city, interval)
main_indexes = get_main_indexes(df_main)
unique_indexes = np.unique(main_indexes)

years = np.reshape( np.array([date[:4] for date in unique_indexes]), -1 )
months = np.reshape( np.array([date[5:7] for date in unique_indexes]), -1 )
monthly_data = {
    'Index': unique_indexes,
    'Ano': years,
    'Mês': months,
    'Casos': get_monthly_cases(df_main, main_indexes, unique_indexes)
}

df_preprocessed = get_monthly_dataframe(monthly_data)

# # Salvando o dataframe
# separador = '\\' if os.name == 'nt' else '/'
# caminho = f'{os.getcwd()}{separador}{city}_monthly.csv'

# df_preprocessed.to_csv(caminho, index=False)