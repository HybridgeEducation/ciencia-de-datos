import pandas as pd

# Cargar archivo descargado de https://www.gob.mx/sesnsp/acciones-y-programas/datos-abiertos-de-incidencia-delictiva
datos = pd.read_csv('../data/sesnsp.csv', encoding='iso-8859-1')

# Convertir a un formato "largo"
datos_long = datos.melt(id_vars=['Año', 'Clave_Ent', 'Entidad', 'Cve. Municipio', 'Municipio', 'Tipo de delito', 'Subtipo de delito'], var_name='nombre_mes', value_name='frecuencia')

# Extraer nombres de meses únicos y crear un DataFrame con números de mes
nombres_meses = datos_long['nombre_mes'].unique()
meses = pd.DataFrame({'nombre': nombres_meses})
meses['numero_mes'] = meses.index + 1

# Crear una columna 'mes' en datos_long con el número de mes correspondiente
datos_long['mes'] = datos_long['nombre_mes'].map(meses.set_index('nombre')['numero_mes'])

# Filtrar filas con frecuencia NA
datos_tidy = datos_long.dropna(subset=['frecuencia'])

# Renombrar columnas
datos_tidy = datos_tidy.rename(columns={
    'Año': 'anio',
    'Clave_Ent': 'clave_entidad',
    'Entidad': 'entidad',
    'Cve. Municipio': 'clave_municipio',
    'Municipio': 'municipio',
    'Tipo de delito': 'tipo_delito',
    'Subtipo de delito': 'subtipo_delito'
})

# Reordenar columnas
datos_tidy = datos_tidy[['anio', 'mes', 'clave_entidad', 'entidad', 'clave_municipio', 'municipio', 'tipo_delito', 'subtipo_delito', 'frecuencia']]

# Guardar archivo
datos_tidy.to_csv('../data/delitos.csv', encoding='utf-8', index=False)
