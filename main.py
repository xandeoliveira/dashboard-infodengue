import streamlit as st
import pandas as pd

# Site para busca do código do município
# https://www.ibge.gov.br/explica/codigos-dos-municipios.php
# REDENÇÃO  2311603
# ACARAPE   2300150

def request_city_info (geocode, ws, we, ys, ye):
  url = "https://info.dengue.mat.br/api/alertcity"
  params =(
      "&disease=dengue&geocode=" + f"{geocode}"
      + "&disease=dengue&format=csv"
      + "&ew_start=" + f"{ws}" + "&ew_end=" + f"{we}"
      + "&ey_start=" + f"{ys}" + "&ey_end=" + f"{ye}"   
  )
  url_resp = "?".join([url, params])

  info = pd.read_csv(url_resp, index_col='SE')

  return info

def get_city_info (city, interval):
  code = {
    "Acarape": 2300150,
    "Redenção": 2311603
  }
  ws, ys, we, ye = interval

  city_info = request_city_info(code[city], ws, we, ys, ye)
  return city_info

# Corpo da interface
menu, main = st.columns([0.3, 0.7])

# Header
with menu:
  city = st.radio("Escolha a cidade:", ["Acarape", "Redenção"])

  st.text("Defina a série temporal:")
  w_start = st.number_input("Semana inicial", 1, 53, 1)
  y_start = st.number_input("Ano inicial", 2010, 2024, 2024)
  w_end = st.number_input("Semana final", 1, 53, 47)
  y_end = st.number_input("Ano final", 2010, 2024, 2024)


# Main
with main:
  st.subheader("Infodengue Acarape/Redenção")
  st.divider()

  interval = (w_start, y_start, w_end, y_end)
  city_info = get_city_info(city, interval)
  
  disaese_cases = city_info[['data_iniSE','casos']]
  st.scatter_chart(disaese_cases, x='data_iniSE', y='casos')
