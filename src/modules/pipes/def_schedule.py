import pandas as pd


# Calcular el schedule mínimo admisible
def calculate_schedule(thickness, sub_df, size):
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
            return schedule


def def_schedule(min_thickness_df, sizes, pipes_dimensions_df):
    # Hacer una copia deñ min_thickness_df
    schedules_df = min_thickness_df.copy()
    pipes_dimensions_df = pipes_dimensions_df.copy()

    # Calcular el schedule para cada espesor
    for size in sizes:
        # Extraer únicamente los schedules de cada tamaño
        sub_df = pipes_dimensions_df[['SIZE', size]]

        # Eliminar los schedules que no existen
        sub_df = sub_df[(sub_df[size] != '-')]

        # Reordenar el sub_df
        sub_df.sort_values(by=[size, 'SIZE'], inplace=True)

        # Calcular el sch para cada diámetro y cada espesor
        schedules_df[size] = schedules_df[size].apply(
            calculate_schedule, sub_df=sub_df, size=size)

    # Guardar el archivo de schedules
    schedules_df.to_csv('./output/pipes_schedules.csv', index=False)
