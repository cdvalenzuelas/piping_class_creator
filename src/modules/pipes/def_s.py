import pandas as pd


from src.utils.write_diagnostic import write_diagnostic


# Interpolar los esfuerzos máximos a la temperatura dada
def iterpolate(row, temp_a, temp_k, temp_b):
    s_a, s_b = row

    if s_a == '-' or s_b == '-':
        return '-'

    return s_b + (s_a - s_b) * (temp_b - temp_k) / (temp_b - temp_a)


def def_s(temperatures, min_temperature, max_temperature, available_pipe_materials):
    # Leer los materiales de tubería
    pipes_materials_df = pd.read_csv(
        './src/elements/pipes/pipes_materials.csv')

    # Filtrar los materiales disponibles
    if len(available_pipe_materials) > 0:
        pipes_materials_df = pipes_materials_df[(
            pipes_materials_df['SPEC_NO'].isin(available_pipe_materials))]

    # Llenar los espacios vacíos
    pipes_materials_df.fillna('-', inplace=True)

    # Ordenar el df
    pipes_materials_df.sort_values(by=['SPEC_NO', 'TYPE/GRADE'], inplace=True)

    # Las temperaturas en las cuales se definen los esfuerzos según ASME B31.3
    temperatures_size = len(temperatures)

    # Inicializar las temperaturas a las cuales se interpolarán los esfuerzos admisibles
    temp_a = None
    temp_k = None
    temp_b = None

    # Definir las temperaturas a las cuales se interpolarán los esfuerzos admisibles
    for index, temp_1 in enumerate(temperatures):
        if index < temperatures_size - 1:
            temp_2 = temperatures[index + 1]

            if max_temperature > temp_2:
                continue

            if temp_1 == max_temperature:
                temp_k = temp_1
                break

            if temp_2 == max_temperature:
                temp_k = temp_2
                break

            if max_temperature > temp_1 and temp_2 > max_temperature:
                temp_a = temp_1
                temp_k = max_temperature
                temp_b = temp_2
                break

    write_diagnostic(f"""
Lo primero es teterminar el valor de S [ksi] para la máxima temperatura de operación ({max_temperature} °F).""")

    # DEFINIR EL VALOR DE 'S' PARA LA TEMPERATURA MÁXIMA DE OPERACIÓN
    if temp_k in temperatures:

        write_diagnostic(f"""
Como la temperatura de operación se encuentra dentro de las establecidas en la norma (tabulada), 
el valor de S [ksi] corresponde a los dados en la columna '{max_temperature}' de la tabla A-1 del código ASME B31.3 EDICIÓN 2020.
""")

        pipes_materials_df['S'] = pipes_materials_df[f'{temp_k}']
    else:

        write_diagnostic(f"""
Como la temperatura de operación no se encuentra dentro de las establecidas en la norma (tabuladas),
el valor de S [ksi] corresponde a la interpolación de valores de S [ksi] teniendo en cuenta dos temperaturas tabuladas. 
Las columnas que se deben tener en cuenta son '{temp_a}' y '{temp_b}' de la tabla A-1 del código ASME B31.3 EDICIÓN 2020.
""")

        pipes_materials_df['S'] = pipes_materials_df[[f'{temp_a}', f'{temp_b}']].apply(
            iterpolate, axis=1, temp_a=temp_a, temp_k=temp_k, temp_b=temp_b)

    pipes_materials_df.drop(['100', '200', '300', '400', '500', '600', '650',
                             '700', '750', '800', '850', '900', '950', '1000', '1050', '1100'], inplace=True, axis=1)

    # Recoger los materiales que no soportan altas temperaturas
    pipes_materials_deleted_by_high_temperature = pipes_materials_df[(
        pipes_materials_df['S'] == '-')]

    pipes_materials_deleted_by_high_temperature = pipes_materials_deleted_by_high_temperature[[
        'SPEC_NO', 'TYPE/GRADE']]

    pipes_materials_deleted_by_high_temperature.to_csv(
        './output/pipes_materials_deleted_by_high_temperature.csv', index=False)

    # Dejar únicamente los que tengan un S válido
    pipes_materials_df = pipes_materials_df[(
        pipes_materials_df['S'] != '-')]

    temp_pipes_materials_df = pipes_materials_df[[
        'SPEC_NO', 'TYPE/GRADE', 'S']]

    write_diagnostic(f"""
Los S [ksi] calculados para cada material son los siguientes:

{temp_pipes_materials_df}
""")

    write_diagnostic(text=f"""
Los siguientes materiales no fueron tenidos en cuenta pues no resisten temperaturas de operación mayores o iguales a {max_temperature} °F:.

{pipes_materials_deleted_by_high_temperature}
""")

    return pipes_materials_df
