from src.modules.flanges.flanges import flanges
from src.modules.pipes.pipes import pipes


def run():
    # En °F
    min_temperature = 32
    # En °F
    max_temperature = 300
    # En psi
    max_pressure = 285
    # En pulgadas
    corrosion_load = 0.125
    # Los schedules disponibles en el mercado
    available_schedules = ['10', '40', 'STD', '80', 'XS', '160', 'XXS']

    # flanges(min_temperature=min_temperature,
    # max_temperature=max_temperature, max_pressure=max_pressure)

    # Definir las posibles combinaciones de materiales, diámetros y espesores de tuberías que cumplen el requerimiento
    pipes(min_temperature=min_temperature,
          max_temperature=max_temperature, max_pressure=max_pressure, corrosion_load=corrosion_load, available_schedules=available_schedules)


if __name__ == '__main__':
    run()
