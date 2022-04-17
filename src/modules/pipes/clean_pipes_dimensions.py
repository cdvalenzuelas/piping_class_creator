import pandas as pd


def clean_pipes_dimensions(available_schedules):
    # Traer las tuberías y sus dimensiones
    pipes_dimensions_df = pd.read_csv(
        './src/elements/pipes/pipes_dimensions.csv')

    # Llenar los vacío
    pipes_dimensions_df.fillna('-', inplace=True)

    # Eliminar los Schedules no comerciales
    if len(available_schedules):
        # Dejar únicamente las columnas necesarias
        size_number_df = pipes_dimensions_df[['SIZE']]

        pipes_dimensions_df = pipes_dimensions_df[available_schedules]

        pipes_dimensions_df = pd.concat(
            [size_number_df, pipes_dimensions_df], axis=1)

    # Hacer la transpuesta del df
    pipes_dimensions_df.set_index(['SIZE'], inplace=True)

    pipes_dimensions_df = pipes_dimensions_df.T

    pipes_dimensions_df.reset_index(inplace=True)

    pipes_dimensions_df.rename(columns={'index': 'SIZE'}, inplace=True)

    # Retornar el pipes_dimensios_df limpio
    return pipes_dimensions_df
