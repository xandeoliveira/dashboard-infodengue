import streamlit as st
import ibge
import infodengue
import datetime
  
# url_factory(2300150, 1, 54, 2024, 2024)
code_cities = ibge.get_formated_dataset()
ufs = ibge.get_unique_UFs(code_cities)

header = st.sidebar.container()
with header:
  header.title("Ajustes")

  period = header.container()
  with period:
    period.header("Período", divider=True)

    current_year = datetime.date.today().year

    start_date = period.date_input("Início",
      min_value="2014-01-01",
      max_value="today",
      value=f"{current_year}-01-01",
      format="DD/MM/YYYY")
    
    end_date = period.date_input("Fim",
      min_value="2024-01-01",
      max_value="today",
      value="today",
      format="DD/MM/YYYY")

  location = header.container()
  with location:
    location.header("Local", divider=True)

    selected_uf = location.selectbox("UF", ufs, index=9)
    cities = ibge.get_cities_by_UF(code_cities, selected_uf)
    selected_city = location.selectbox("Município", cities['name'], index=None, placeholder="Escolha o município")

  view_button = header.button("Visualizar", type="secondary", use_container_width=True)

main = st.container()
with main:
  main.header("Casos de dengue em cidades brasileiras", divider=True)
  city_and_uf_header = main.subheader("")

  chart_area = main.empty()
  with chart_area:
    chart_area.text("Para renderizar as informações que deseja, ajuste todos os parâmetros.")

if (view_button):
  try:
    params = {
      "geocode": ibge.get_code_by_city(code_cities, selected_city),
      "ey_start": str(start_date.year),
      "ey_end": str(end_date.year)}
    
    city_data = infodengue.get_formated_dataset(params)
    city_data = infodengue.get_city_data(city_data, start_date, end_date)

    df_plot = city_data[["data_iniSE", "casos"]]
    
    city_and_uf_header.text(f"{selected_city}, {selected_uf}")
    chart_area.line_chart(df_plot,
                          x="data_iniSE",
                          y="casos",
                          use_container_width=True,
                          x_label="Data",
                          y_label="Número de casos")

  except:
    chart_area.warning("Nem todos os dados de busca foram preenchidos.", icon="⚠️")
