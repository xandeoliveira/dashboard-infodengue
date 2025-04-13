from pandas import read_csv

def get_formated_dataset():
  return read_csv("../datasets/code_cities.csv")

def get_unique_UFs(code_cities):
  return code_cities['UF'].unique()

def get_cities_by_UF(code_cities, UF):
  return code_cities[ code_cities['UF'] == UF ]

def get_code_by_city(code_cities, city):
  df_city = code_cities[ code_cities['name'] == city ]
  array_code = df_city['code']
  code = array_code.values[0]

  return str(code)