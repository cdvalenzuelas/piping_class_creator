from src.utils.write_diagnostic import write_diagnostic


# Eliminar los espesores menores al límite
def def_thk_limits(row, size):
    spec, grade, gt, lt, thickness = row

    if gt == '-':
        return thickness

    if thickness > gt * 25.4 or thickness < lt * 25.4:
        return thickness
    else:
        print('OJOOOOOOOOOOOOOOOOOOOOO')
        with open('./output/asme_b31_3_table_A1_thickness_limitations.csv', mode='a') as f:
            f.write('{spec}, {grade}, {size}, {gt}, {lt}, {thickness}\n')

        return '-'


def def_size_limits(code_thickness_df, sizes):
    write_diagnostic(f"""
Finálmente se tienen en cuenta las limitaciones de espesor dadas por la tabla A-1 del código ASME B31.3 edición 2020. Es decir, 
no se tienen en cuenta combinaciones de material y diámetro (NPS) que cuenten con espesores mayores o menores a los
establecidos en la tabla mensionada anteiormente. Estas combinaciones de material, diámetro y espsor están dadas en el archivo
'asme_b31_3_table_A1_thickness_limitations.csv'.""")

    # Crear el archi eliminados por limitaciones espesor tabla A-1 asme B31.3
    with open('./output/asme_b31_3_table_A1_thickness_limitations.csv', mode='a') as f:
        f.write('"SPEC_NO", TYPE/GRADE, SIZE, MIN_THK, MAX_THK, thickness\n')

    # Hacer una copia del df
    code_thickness_df = code_thickness_df.copy()

    # Ver las limitaciones de tamaño por cada diámetro
    for size in sizes:
        # Eliminar los diámetros menores al límite
        code_thickness_df[size] = code_thickness_df[[
            'SPEC_NO', 'TYPE/GRADE', 'MIN_THK', 'MAX_THK', size]].apply(def_thk_limits, axis=1, size=size)

    # Guardar el archivo de code thickness
    code_thickness_df.to_csv(
        './output/pipes_code_thickness.csv', index=False)
