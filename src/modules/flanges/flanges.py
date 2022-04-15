from ast import Return
import pandas as pd


def flanges(min_temperature, max_temperature, max_pressure):
    # Leer el archivo de flanges
    materials_group_1_1 = pd.read_csv(
        './src/elements/flanges/materials_group_1.1.csv')

    # Indice fina
    final_index = materials_group_1_1.shape[0] - 1

    # Temperatura inicial y temperatura final
    t_start = materials_group_1_1.loc[0, 'temperature']
    t_final = materials_group_1_1.loc[final_index, 'temperature']

    # Verificar si la temperatura mínima de operación está en los rangos
    if min_temperature < t_start:
        print('LA TEMPERATURA MÍNIMA DE OPERACIÓN ESTÁ POR DEBAJO DE LA TEMPERATURA DE OPERACIÓN DE LAS BRIDAS')

    if max_temperature > t_final:
        print('LA TEMPERATURA MÁXIMA DE OPERACIÓN ESTÁ POR ENCIMA DE LA TEMPERATURA DE OPERACIÓN DE LAS BRIDAS')

    # Ver los límites de temperatura
    materials_group_1_1.reset_index()

    t_min = None
    t_max = None

    for index, row in materials_group_1_1.iterrows():
        if index < final_index - 1:
            index_a, temperature_a, class_150_a, class_300_a, class_600_a, class_900_a, class_1500_a, class_2500_a = materials_group_1_1.iloc[
                index]
            index_b, temperature_b, class_150_b, class_300_b, class_600_b, class_900_b, class_1500_b, class_2500_b = materials_group_1_1.iloc[
                index + 1]

            if temperature_a == t_start:
                t_min = temperature_a
            elif temperature_b == t_final:
                t_max = temperature_b
            elif min_temperature > temperature_a and min_temperature < temperature_b:
                t_min = temperature_a
            elif max_temperature > temperature_a and max_temperature < temperature_b:
                t_max = temperature_b

    # Filtrar el dataframe por temperaturas
    materials_group_1_1 = materials_group_1_1[(materials_group_1_1['temperature'] <= t_max) & (
        materials_group_1_1['temperature'] >= t_min)]

    rating = None

    # Seleccionar la clase correcta
    if materials_group_1_1['150'].max() >= max_pressure:
        rating = 150
    elif materials_group_1_1['300'].max() >= max_pressure:
        rating = 300
    elif materials_group_1_1['600'].max() >= max_pressure:
        rating = 600
    elif materials_group_1_1['900'].max() >= max_pressure:
        rating = 900
    elif materials_group_1_1['1500'].max() >= max_pressure:
        rating = 1500
    elif materials_group_1_1['2500'].max() >= max_pressure:
        rating = 2500

    if rating == None:
        print('LAS BRIDAS NO SOPORTAN ESTA PRESIÓN PARA ESTOS RANGOS DE TEMPERATURAS')
    else:
        print(f'TEMPERATURA MÍNIMA DE OPERACIÓN: {min_temperature}°F')
        print(f'TEMPERATURA MÁXIMA DE OPERACIÓN: {max_temperature}°F')
        print(f'PRESIÓN MÁXIMA DE OPERACIÓN: {max_pressure}psig')
        print('-----------------------------------------------------')
        print(f'EL RATING SELECCIONADO ES #{rating}')
        print('-----------------------------------------------------')

        materials_group_1_1 = materials_group_1_1[[
            'materials_group', 'temperature', f'{rating}']]
        print(materials_group_1_1)

    print(rating)

    return rating
