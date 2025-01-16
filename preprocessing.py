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
    info = pd.read_csv(url_resp)
    return info

def get_city_info(city, interval):
    code = {
        "Acarape": 2300150,
        "Redenção": 2311603
    }
    ws, ys, we, ye = interval

    city_info = request_city_info(code[city], ws, we, ys, ye)

    se = city_info['SE']
    city_info.drop(columns=['SE','casos_est','casos_est_min','casos_est_max',
                            'Localidade_id','id','versao_modelo','tweet',
                            'casprov','casprov_est','casprov_est_min',
                            'casprov_est_max','casconf'], inplace=True)
    return city_info, se

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

        tempmin.append(weeks['tempmin'].mean())
        tempmed.append(weeks['tempmed'].mean())
        tempmax.append(weeks['tempmax'].mean())

        umidmin.append(weeks['umidmin'].mean())
        umidmed.append(weeks['umidmed'].mean())
        umidmax.append(weeks['umidmax'].mean())

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

def get_additional_stats(df, unique_indexes):
    # Obtendo as estatísticas adicionais de p_rt1, p_inc100k, Rt, receptivo, transmissao e nivel_inc
    df = df[['data_iniSE','p_rt1','p_inc100k','Rt','receptivo','transmissao','nivel_inc']]
    p_rt1 = list()
    p_inc100k = list()
    Rt = list()
    receptivo = list()
    transmissao = list()
    nivel_inc = list()

    for month in unique_indexes:
        weeks = df[df['data_iniSE'] == month]
        p_rt1.append(weeks['p_rt1'].mean())
        p_inc100k.append(weeks['p_inc100k'].mean())
        Rt.append(weeks['Rt'].mean())
        receptivo.append(weeks['receptivo'].mode()[0])
        transmissao.append(weeks['transmissao'].mode()[0])
        nivel_inc.append(weeks['nivel_inc'].mode()[0])

    additional_stats = {
        'p_rt1': p_rt1, 'p_inc100k': p_inc100k, 'Rt': Rt,
        'receptivo': receptivo, 'transmissao': transmissao, 'nivel_inc': nivel_inc
    }
    return additional_stats

def save_df(df, name):
    spacer = '\\' if os.name == 'nt' else '/'
    caminho = f'{os.getcwd()}{spacer}datasets{spacer}{name}'
    df.to_csv(caminho, index=False)


# PRÉ-PROCESSAMENTO PARA O INTERVALO DE EXEMPLO
def preprocessing (city):
    interval = (1, 2014, 53, 2024)

    df_main, se = get_city_info(city, interval)
    main_indexes = get_main_indexes(df_main)

    df_main.loc[:, 'data_iniSE'] = main_indexes
    unique_indexes = np.unique(main_indexes)

    indexes_data = {
        'ME': unique_indexes,
        'ano': np.reshape( np.array([date[:4] for date in unique_indexes]), -1 ),
        'mês': np.reshape( np.array([date[5:7] for date in unique_indexes]), -1 ),
    }

    monthly_temp_and_hum = get_monthly_temp_and_hum(df_main, unique_indexes)
    level_pop_and_accum = get_level_pop_and_accum(df_main, unique_indexes)
    additional_stats = get_additional_stats(df_main, unique_indexes)

    monthly_data = {
        **indexes_data,
        'casos': get_monthly_cases(df_main, unique_indexes),
        **monthly_temp_and_hum,
        **level_pop_and_accum,
        **additional_stats
    }

    df_main.loc[:, 'data_iniSE'] = se
    df_main.rename(columns={'data_iniSE': 'SE'}, inplace=True)
    save_df(df_main, city+"_weekly.csv")

    save_df(pd.DataFrame(data=monthly_data), city+"_monthly.csv")

# Finalizando o pré-processamento
preprocessing("Redenção")
preprocessing("Acarape")
