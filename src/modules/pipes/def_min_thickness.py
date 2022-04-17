import pandas as pd


# Calcular esperores
def calculate_thickness(row, max_pressure):
    S, OD = row

    E = 1

    W = 1

    Y = 1

    # Los valores de esfuerzo máximo se expresan en ksi
    P = max_pressure / 1000

    thickness = 0.5 * (P * OD) / (S*E*W + P*Y)

    if (thickness >= OD / 6) or (P / (S * E) > 0.385):
        return '-'

    return round(thickness, 4)


def add_corrosion_load(thickness, corrosion_load):
    if thickness == '-':
        return '-'

    return round(thickness + 25.4 * corrosion_load, 4)


def def_min_thickness(max_pressure, pipes_materials_df, corrosion_load):
    # Hacer una copia
    pipes_materials_df = pipes_materials_df.copy()

    # Traer las tuberías y sus dimensiones
    pipes_dimensions = pd.read_csv(
        './src/elements/pipes/pipes_dimensions.csv')

    # Llenar vacíos
    pipes_dimensions.fillna('-', inplace=True)

    # Dejar únicamente el nombre del diámetro y su diámetro esxterior
    pipes_dimensions = pipes_dimensions[['SIZE', 'OD']]

    pipes_dimensions.set_index(['SIZE'], inplace=True)

    pipes_dimensions = pipes_dimensions.T

    # Sacar todos los diámetros seleccionados por ingeniería
    sizes = pipes_dimensions.columns

    # Concatenar los dos dataframes
    min_thickness_df = pd.concat(
        [pipes_materials_df, pipes_dimensions], axis=1)

    min_thickness_df.fillna(method='bfill', inplace=True)

    # Eliminar la última tupla (sale nula)
    min_thickness_df = min_thickness_df[(
        min_thickness_df['MATERIAL'].notnull())]

    # Ordenar el df
    min_thickness_df.sort_values(by=['SPEC_NO', 'TYPE/GRADE'], inplace=True)

    # Calcular los espesores para cada uno de los diámetros
    for size in sizes:
        min_thickness_df[size] = min_thickness_df[['S', size]].apply(
            calculate_thickness, axis=1, max_pressure=max_pressure)

    # Guardar el archivo de espesores mínimos
    min_thickness_df.to_csv('./output/pipes_min_thickness.csv', index=False)

    # Adicionar la carga de corrosión
    for size in sizes:
        min_thickness_df[size] = min_thickness_df[size].apply(
            add_corrosion_load, corrosion_load=corrosion_load)

    # Guardar el archivo de espesores con la adición de la carga de corrosión
    min_thickness_df.to_csv(
        './output/pipes_thickness_with_corrosion_load.csv', index=False)

    return (min_thickness_df, sizes)
