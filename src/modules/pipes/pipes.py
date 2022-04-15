import pandas as pd


from src.modules.pipes.def_s import def_s
from src.modules.pipes.def_thickness import def_thickness
from src.modules.pipes.def_schedules import def_schedules


def pipes(min_temperature, max_temperature, max_pressure, corrosion_load, available_schedules):

    # Estas temperaturas están establecidas en la norma ASME B31.3
    temperatures = [100, 200, 300, 400, 500, 600, 650,
                    700, 750, 800, 850, 900, 950, 1000, 1050, 1100]

    if max_temperature > max(temperatures):
        print('LA MÁXIMA TEMPERATURA DE OPERACIÓN ESTÁ POR FUERA DEL RANGO DE OPERACIÓN DE LAS TUBERÍAS')
    else:
        # Definir el valor de S en función de la máxima temperatura de operación y traer el df limpio (con la columna 'S')
        pipes_materials_df = def_s(temperatures=temperatures, min_temperature=min_temperature,
                                   max_temperature=max_temperature)

        # Definir el espesor mínimo de la tubería en función del material. trae los espesores calculados y los diámetros
        thickness_df, sizes = def_thickness(max_pressure=max_pressure,
                                            pipes_materials_df=pipes_materials_df, corrosion_load=corrosion_load)

        # Definir los schedules para cada espesor
        def_schedules(thickness_df=thickness_df, sizes=sizes,
                      available_schedules=available_schedules)

        # Aquí se revisan los límirtes de tamaño para las tuberías
