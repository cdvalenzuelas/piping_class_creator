import shutil
import os

from src.modules.flanges.flanges import flanges
from src.modules.pipes.pipes import pipes
from src.utils.write_diagnostic import write_diagnostic


def run():
    # En °F
    min_temperature = 32
    # En °F
    max_temperature = 720
    # En psi
    max_pressure = 3000
    # En pulgadas
    corrosion_load = 0.0625
    # Definir los materiales disponibles para tubería
    available_pipe_materials = ['A106', 'API 5L', 'A333', 'A53']
    # Los schedules disponibles en el mercado
    available_schedules = ['10', '40', 'STD', '80', 'XS', '160', 'XXS']

    # Eliminar los archivos de la carpeta output
    try:
        shutil.rmtree('output')

        os.mkdir('output')
    except:
        pass

        # Iniciar el piping class
    write_diagnostic(f"""
Se genera una spec con las siguientes condiciones iniciales:

* Temperatura mínima de operación de {min_temperature} °F.
* Temperatura máxima de operación de {max_temperature} °F.
* Presión máxima de operación de {max_pressure} psig.
* Una corrosión permisible de {corrosion_load} in.
* Los materiales disponibles para la tubería son los siguientes: {available_pipe_materials}.
* Los schedules disponibles para la tubería son los siguientes: {available_schedules}
""")

    # Definir el rating de las bridas
    flanges(min_temperature=min_temperature,
            max_temperature=max_temperature,
            max_pressure=max_pressure)

    # Definir las posibles combinaciones de materiales, diámetros y espesores de tuberías que cumplen el requerimiento
    pipes(min_temperature=min_temperature,
          max_temperature=max_temperature,
          max_pressure=max_pressure,
          corrosion_load=corrosion_load,
          available_schedules=available_schedules,
          available_pipe_materials=available_pipe_materials)


if __name__ == '__main__':
    run()
