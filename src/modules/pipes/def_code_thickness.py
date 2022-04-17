import pandas as pd

# Calcualr el espesor mínimo relacionado a un schedule


def calculate_code_thickness(thickness, sub_df, size):
    if thickness == '-':
        return '-'

    # Hacerle una copia sl sub_df
    sub_df = sub_df.copy()

    # Eliminar los SCH con un thickness nominal menor al calculado
    sub_df = sub_df[(sub_df[size] > thickness)]

    # Ver el tamaño del sub_df
    sub_df_size = sub_df.shape[0]

    # Si no hay schedules para ese espesor entonces retornar un '-'
    if sub_df_size == 0:
        return '-'

    for index, row in sub_df.iterrows():
        schedule, code_thickness = row

        if code_thickness >= thickness:
            return code_thickness


def def_code_thickness(min_thickness_df, sizes, pipes_dimensions_df):
    # Hacer una copia de los df
    code_thickness_df = min_thickness_df.copy()
    pipes_dimensions_df = pipes_dimensions_df.copy()

    # Calcular el code thickness
    for size in sizes:
        # Extraer únicamente los schedules de cada tamaño
        sub_df = pipes_dimensions_df[['SIZE', size]]

        # Eliminar los schedules que no existen
        sub_df = sub_df[(sub_df[size] != '-')]

        # Reordenar el sub_df
        sub_df.sort_values(by=[size, 'SIZE'], inplace=True)

        # Calcular el sch para cada diámetro y cada espesor
        code_thickness_df[size] = code_thickness_df[size].apply(
            calculate_code_thickness, sub_df=sub_df, size=size)

    # Retornar el df calculado para revisar las limitaciones de espesor y diámetro
    return code_thickness_df
