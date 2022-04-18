from src.modules.pipes.def_s import def_s
from src.modules.pipes.def_min_thickness import def_min_thickness
from src.modules.pipes.clean_pipes_dimensions import clean_pipes_dimensions
from src.modules.pipes.def_code_thickness import def_code_thickness
from src.modules.pipes.def_size_limits import def_size_limits
from src.modules.pipes.def_schedule import def_schedule
from src.utils.write_diagnostic import write_diagnostic


def pipes(min_temperature, max_temperature, max_pressure, corrosion_load, available_schedules, available_pipe_materials):
    write_diagnostic(f"""
2. TUBERÍAS
___________""")

    # Estas temperaturas están establecidas en la norma ASME B31.3
    temperatures = [100, 200, 300, 400, 500, 600, 650,
                    700, 750, 800, 850, 900, 950, 1000, 1050, 1100]

    if max_temperature > max(temperatures):
        print('❌ LA MÁXIMA TEMPERATURA DE OPERACIÓN ESTÁ POR FUERA DEL RANGO DE OPERACIÓN DE LOS MATERIALES TENIDOS EN CUENTA')

        write_diagnostic(f"""
La temperatura máxima de operación está por fuera del rango de operación de los materiales de tubería tenidos en cuenta.""")

    else:
        # Definir el valor de S en función de la máxima temperatura de operación y traer el df limpio (con la columna 'S')
        pipes_materials_df = def_s(temperatures=temperatures,
                                   min_temperature=min_temperature,
                                   max_temperature=max_temperature,
                                   available_pipe_materials=available_pipe_materials)

        # Definir el espesor mínimo de la tubería en función del material. trae los espesores calculados y los diámetros
        min_thickness_df, sizes = def_min_thickness(max_pressure=max_pressure,
                                                    pipes_materials_df=pipes_materials_df,
                                                    corrosion_load=corrosion_load)

        # Limpiar el pupes_dimensios para calcular los espesores por código, los sch y tener en cuenta las limitaciones dimensionales de los materiales
        pipes_dimensions_df = clean_pipes_dimensions(
            available_schedules=available_schedules)

        # Definir el espesor mínimo de tubería según un sch
        code_thickness_df = def_code_thickness(min_thickness_df=min_thickness_df,
                                               sizes=sizes,
                                               pipes_dimensions_df=pipes_dimensions_df)

        # Definir los límites de diámetro por material
        def_size_limits(code_thickness_df=code_thickness_df,
                        sizes=sizes)

        # Definir los sch mínimos para cada material dependiendo de las condiciones de presión y temperatura
        def_schedule(min_thickness_df=min_thickness_df,
                     sizes=sizes,
                     pipes_dimensions_df=pipes_dimensions_df)
