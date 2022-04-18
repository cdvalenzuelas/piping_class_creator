import pandas as pd

from src.utils.write_diagnostic import write_diagnostic


# Calcular esperores
def calculate_thickness(row, max_pressure, size):
    spec, grade, S, OD = row

    E = 1

    W = 1

    Y = 1

    # Los valores de esfuerzo máximo se expresan en ksi
    P = max_pressure / 1000

    thickness = 0.5 * (P * OD) / (S*E*W + P*Y)

    if (thickness >= OD / 6) or (P / (S * E) > 0.385):
        # Escribir el archivo
        with open('./output/asme_b31_3_304_1_2_limitations.csv', mode='a') as f:
            f.write(
                f'"{spec}", {grade}, {size}, {round(OD/thickness, 4)}, {round(P/(S*E), 4)}\n')

        return '-'

    return round(thickness, 4)


def add_corrosion_load(thickness, corrosion_load):
    if thickness == '-':
        return '-'

    return round(thickness + 25.4 * corrosion_load, 4)


def def_min_thickness(max_pressure, pipes_materials_df, corrosion_load):
    write_diagnostic(f"""
Una vez se tienen los materiales válidos para el cálculo, es decir, que la tempera máxima de operación del sistema se encuentre
dentro de las temperaturas de operación del material de la tubería, se procede a calcular el espesor mínimo de pared
para cada combinación de diámetro nominal (NPS) y material.

Los cálculos de espesores corresponden a la plicación de la fórmula dada en el parágrafo 304.1.2 del código ASME B31.3 edición 2020.La formula
descrita en este parágrafo es la siguiente:

            t=P*D
    t = ---------------
        2*(S*E*W + Y*P)

En donde:

* P representa la presión interna de la tubería (presión máxima de operación del sistema).
* D representa en diámetro externo de la tubería.
* t representa el espesor mínimo de diseño para tuberías con presión interna.
* S representa el valor de esfuerzo de cada material (calculado en pasos anteriores) extraido de la tabla A-1 del código ASME B31.3 edición 2020.
* E representa el factor de calidad extraido de la tabla A-1A del código ASME B31.3 edición 2020.
* W representa el facor de reducción de resistencia del material de acuerdo con el parágrafo 302.3.5(e) del código ASME B31.3 edición 2020.
* Y representa el coeficiente extrído del parágrafo 304.1.1 del código ASME B31.3 edición 2020. Estos valores son válidos para t<D/6.

El resultado de estos cálculos se puede observar en el archivo 'pipes_min_thickness.csv'.

Este cálculo por este método tienen dos limitaciones importante y no son cubiertas por el código ASME B31.3 edición 2020. Estas son las siguientes:

1. El material de tubería que cuente con un espesor de tuberías calculado mayor a D/6 no debe ser considerado viable.
2. El material de tubería que cunete con una razón de P/(S*E) mayor a 0.385 (factor de seguridad) no debe ser considerado.

Los materiales que cumplen con las una o las dos condiciones anteriores (materiales a no ser tenidos en cuenta) están
consignados en el archivo 'asme_b31_3_304_1_2_limitations.csv'.

Luego de haber calculado los espesores mínimos de diseño, se procede a adicionar la corrosión adimisble, es decir {corrosion_load} in 
ó {round(corrosion_load *25.4 ,4)} mm. El resultado de esta suma se encuentra en ela rchivo 'pipes_thickness_with_corrosion_load.csv'.
""")

    # Crear el archi eliminados por limitaciones del parágrafo 304.1.2 del código asme B31.3 ediición 2020
    with open('./output/asme_b31_3_304_1_2_limitations.csv', mode='a') as f:
        f.write('"SPEC_NO", TYPE/GRADE, SIZE, D/t, P/(S*E)\n')

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
        min_thickness_df[size] = min_thickness_df[['SPEC_NO', 'TYPE/GRADE', 'S', size]].apply(
            calculate_thickness, axis=1, max_pressure=max_pressure, size=size)

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
