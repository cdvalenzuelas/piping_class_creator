# Eliminar los espesores menores al límite
def def_min_thk(row):
    gt, thickness = row

    if gt == '-':
        return thickness

    if thickness > gt * 25.4:
        return thickness
    else:
        return '-'


# Eliminar los espesores mayores al límite
def def_max_thk(row):
    lt, thickness = row

    if lt == '-':
        return thickness

    if thickness < lt * 25.4:
        return thickness
    else:
        return '-'


def def_size_limits(code_thickness_df, sizes):
    # Hacer una copia del df
    code_thickness_df = code_thickness_df.copy()

    # Ver las limitaciones de tamaño por cada diámetro
    for size in sizes:
        # Eliminar los diámetros menores al límite
        code_thickness_df[size] = code_thickness_df[[
            'MIN_THK', size]].apply(def_min_thk, axis=1)

        # Eliminar los diámetros mayores al límite
        code_thickness_df[size] = code_thickness_df[[
            'MAX_THK', size]].apply(def_max_thk, axis=1)

    # Guardar el archivo de code thickness
    code_thickness_df.to_csv(
        './output/pipes_code_thickness.csv', index=False)
