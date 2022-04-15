import pandas as pd


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


def def_schedules(thickness_df, sizes, available_schedules):
    # Haciendo una copia del archivo thickness
    schedules_df = thickness_df.copy()

    # Traer las tuberías y sus dimensiones
    pipes_dimensions = pd.read_csv(
        './src/elements/pipes/pipes_dimensions.csv')

    # Llenar los vacío
    pipes_dimensions.fillna('-', inplace=True)

    # Dejar únicamente las columnas necesarias
    pipes_dimensions.drop(['OD', 'SIZE_NUMBER'], inplace=True, axis=1)

    # Redefinir el index
    pipes_dimensions.set_index(['SIZE'], inplace=True)

    # Eliminar los Schedules no comerciales
    if len(available_schedules):
        pipes_dimensions = pipes_dimensions[available_schedules]

    # Hacerle una transpuesta al df (dejar los diámetros como nombres de columnas y los sch como filas)
    pipes_dimensions = pipes_dimensions.T

    # Resetear el indice
    pipes_dimensions.reset_index(inplace=True)

    # Renombrar el indice
    pipes_dimensions.rename(columns={'index': 'SIZE'}, inplace=True)

    # Calcular el schedule para cada espesor
    for size in sizes:
        # Extraer únicamente los schedules de cada tamaño
        sub_df = pipes_dimensions[['SIZE', size]]

        # Eliminar los schedules que no existen
        sub_df = sub_df[(sub_df[size] != '-')]

        # Reordenar el sub_df
        sub_df.sort_values(by=[size, 'SIZE'], inplace=True)

        # Calcular el sch para cada diámetro y cada espesor
        schedules_df[size] = schedules_df[size].apply(
            calculate_schedule, sub_df=sub_df, size=size)

    # Guardar el archivo de schedules
    schedules_df.to_csv('./output/pipes_schedules.csv', index=False)
