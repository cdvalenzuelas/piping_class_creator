import shutil
import os

from src.modules.flanges.flanges import flanges
from src.modules.pipes.pipes import pipes


def run():
    # En °F
    min_temperature = 32
    # En °F
    max_temperature = 200
    # En psi
    max_pressure = 2200
    # En pulgadas
    corrosion_load = 0.0625
    # Los schedules disponibles en el mercado
    available_schedules = ['10', '40', 'STD', '80', 'XS', '160', 'XXS']

    # Eliminar los archivos de la carpeta output
    try:
        shutil.rmtree('output')

        os.mkdir('output')
    except:
        pass

    # Definir el rating de las bridas
    flanges(min_temperature=min_temperature,
            max_temperature=max_temperature, max_pressure=max_pressure)

    # Definir las posibles combinaciones de materiales, diámetros y espesores de tuberías que cumplen el requerimiento
    pipes(min_temperature=min_temperature,
          max_temperature=max_temperature, max_pressure=max_pressure, corrosion_load=corrosion_load, available_schedules=available_schedules)


if __name__ == '__main__':
    run()
