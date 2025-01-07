import pandas as pd
import numpy as np
import os

# FUNÇÕES DE API
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


# FUNÇÕES DE "CONVERSÃO"
def get_main_indexes(df):
  # data_iniSE no formato YYYY-MM-DD, convertendo para MM-YYYY
  df = df[['data_iniSE']]
  dates = list()

  for date in df.loc[:, 'data_iniSE']:
    dates.append(date[:7])

  df.loc[:, 'data_iniSE'] = dates

  return dates

def get_monthly_cases(df, unique_indexes):
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

def get_monthly_temp_and_hum(df, unique_indexes):
  # Tirando as médias para um mesmo mês
  df = df[['data_iniSE','tempmin','tempmed','tempmax','umidmin','umidmed','umidmax']]
  tempmin = list()
  tempmed = list()
  tempmax = list()
  umidmin = list()
  umidmed = list()
  umidmax = list()

  for month in unique_indexes:
    weeks = df[df['data_iniSE'] == month]

    tempmin.append(weeks['tempmin'].sum() / len(weeks['tempmin']))
    tempmed.append(weeks['tempmed'].sum() / len(weeks['tempmed']))
    tempmax.append(weeks['tempmax'].sum() / len(weeks['tempmax']))

    umidmin.append(weeks['umidmin'].sum() / len(weeks['umidmin']))
    umidmed.append(weeks['umidmed'].sum() / len(weeks['umidmed']))
    umidmax.append(weeks['umidmax'].sum() / len(weeks['umidmax']))

  monthly_temp_and_hum = {
    'tempmin': tempmin, 'tempmed': tempmed, 'tempmax': tempmax,
    'umidmin': umidmin, 'umidmed': umidmed, 'umidmax': umidmax
    }
  
  return monthly_temp_and_hum

def get_level_pop_and_accum(df, unique_indexes):
  # Obtendo a população e os casos anuais
  df = df[['data_iniSE','nivel','pop','notif_accum_year']]
  levels = list()
  pop = list()
  accum = list()

  for month in unique_indexes:
    weeks = df[df['data_iniSE'] == month]
    levels.append(weeks['nivel'].max())
    pop.append(weeks['pop'].max())
    accum.append(weeks['notif_accum_year'].max())
  
    level_pop_and_accum = { 'nível': levels, 'população': pop, 'casos_acumulados_ano': accum }

  return level_pop_and_accum

# PRÉ-PROCESSAMENTO PARA O INTERVALO DE EXEMPLO
interval = (1, 2024, 53, 2024)
city = "Acarape"

df_main = get_city_info(city, interval)
main_indexes = get_main_indexes(df_main)

df_main.loc[:, 'data_iniSE'] = main_indexes
unique_indexes = np.unique(main_indexes)

indexes_data = {
    'Index': unique_indexes,
    'ano': np.reshape( np.array([date[:4] for date in unique_indexes]), -1 ),
    'mês': np.reshape( np.array([date[5:7] for date in unique_indexes]), -1 ),
}
monthly_temp_and_hum = get_monthly_temp_and_hum(df_main, unique_indexes)
level_pop_and_accum = get_level_pop_and_accum(df_main, unique_indexes)

monthly_data = {
    **indexes_data,
    'casos': get_monthly_cases(df_main, unique_indexes),
    **monthly_temp_and_hum,
    **level_pop_and_accum
}

# Dados pré-processados
df_preprocessed = get_monthly_dataframe(monthly_data)

# SALVANDO O DATAFRAME
separador = '\\' if os.name == 'nt' else '/'
caminho = f'{os.getcwd()}{separador}{city}_monthly.csv'

df_preprocessed.to_csv(caminho, index=False)