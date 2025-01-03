import pandas as pd
import numpy as np

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
    return city_info

def get_monthly_cases(city, interval):
    # Obtenção da informação por cidade e filtrando data e casos
    df = get_city_info(city, interval)
    df = df[['data_iniSE', 'casos']]

    # Listas para formar o dataframe para valores mensais
    months = list()
    month_cases = list()

    # data_iniSE no formato YYYY-MM-DD, convertendo para MM/YYYY
    for date in df.loc[:, 'data_iniSE']:
        year, month, _ = date.split("-")
        months.append(f"{month}/{year}")

    df.loc[:, 'data_iniSE'] = months

    # Somando os casos para um mesmo mês
    unique_months = np.unique(months)
    for month in unique_months:
        weeks = df[df['data_iniSE'] == month]
        month_cases.append(weeks['casos'].sum())

    # Criando o DataFrame com o formato desejado
    dict_months = {"Mês/Ano": unique_months, "Casos": month_cases}
    df_months = pd.DataFrame(dict_months)

    # Salvando o DataFrame em CSV
    df_months.to_csv(f'{city}_monthly_cases.csv', index=False)
    print(f'Dados mensais salvos em {city}_monthly_cases.csv')

    return df_months

# Exemplo de uso
interval = (1, 2014, 40, 2025)
city = "Acarape"
monthly_data = get_monthly_cases(city, interval)
print(monthly_data)

#organizando os casos por ano

arq = 'C:\\Users\\Ivina\\Desktop\\LTSM-bolsa\\redenção.csv'
df=pd.read_csv(arq)

# Separar "Mês/Ano" em colunas separadas para "Mês" e "Ano"
df[['Mês', 'Ano']] = df['Mês/Ano'].str.split('/', expand=True)

df['Ano'] = df['Ano'].astype(int)
data_sorted = df.sort_values(by=['Ano', 'Mês'])

data_sorted = data_sorted[['Ano', 'Mês', 'Casos']]
caminho = 'C:\\Users\\Ivina\\Desktop\\LTSM-bolsa\\redenção_sorted.csv'
data_sorted.to_csv(caminho, index=False)

