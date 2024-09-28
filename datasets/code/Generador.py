import pandas as pd
import numpy as np
import random
from scipy.spatial.distance import euclidean
# Definir el tamaño del DataFrame
num_estaciones = 100
num_tanques = 300
num_valvulas = 750
num_usuarios = 1500
num_aristas = 2500
# Función para generar coordenadas aleatorias con separación mínima
def generar_coordenadas_existentes(n, min_dist=10):
    coords = []
    
    for _ in range(n):
        while True:
            x, y = np.random.uniform(0, 100, 2)  # Generar coordenadas aleatorias
            if all(euclidean((x, y), coord) >= min_dist for coord in coords):
                coords.append((x, y))
                break
    return coords

# Generar coordenadas para las estaciones, tanques, válvulas y usuarios
#coords_estaciones = generar_coordenadas_existentes(num_estaciones)
#coords_tanques = generar_coordenadas_existentes(num_tanques)
#coords_valvulas = generar_coordenadas_existentes(num_valvulas)
#coords_usuarios = generar_coordenadas_existentes(num_usuarios)

# Crear DataFrame de estaciones
estaciones = [f'EST-{i+1:03d}' for i in range(num_estaciones)]
data_estaciones = {
    'ID Estación': estaciones,
    'Capacidad (m³/día)': np.random.randint(1000, 5000, size=num_estaciones),
    'Consumo (m³/día)': np.random.randint(500, 4000, size=num_estaciones),
    'Estado': np.random.choice(['Operativo', 'En reparación', 'Fuera de servicio'], size=num_estaciones),
    #'Coordenadas': coords_estaciones
}
df_estaciones = pd.DataFrame(data_estaciones)

# Crear DataFrame de tanques
tanques = [f'TAN-{i+1:03d}' for i in range(num_tanques)]
data_tanques = {
    'ID Tanque': tanques,
    'Capacidad (m³)': np.random.randint(5000, 20000, size=num_tanques),
    #'Coordenadas': coords_tanques
}
df_tanques = pd.DataFrame(data_tanques)

# Crear DataFrame de válvulas
valvulas = [f'VAL-{i+1:03d}' for i in range(num_valvulas)]
data_valvulas = {
    'ID Válvula': valvulas,
    'Capacidad Control (m³/día)': np.random.randint(100, 1000, size=num_valvulas),
    #'Coordenadas': coords_valvulas
}
df_valvulas = pd.DataFrame(data_valvulas)

# Crear DataFrame de usuarios finales
usuarios = [f'USR-{i+1:03d}' for i in range(num_usuarios)]
data_usuarios = {
    'ID Usuario': usuarios,
    'Consumo Mensual (m³)': np.random.randint(10, 300, size=num_usuarios),
    #'Coordenadas': coords_usuarios
}
df_usuarios = pd.DataFrame(data_usuarios)

# Mostrar los DataFrames
print("Estaciones:")
print(df_estaciones)
print("\nTanques:")
print(df_tanques)
print("\nVálvulas:")
print(df_valvulas)
print("\nUsuarios Finales:")
print(df_usuarios)
print("xd")
df_estaciones.to_excel("data_estaciones.xlsx", sheet_name="estaciones", index=False)
df_tanques.to_excel("data_tanques.xlsx", sheet_name="tanques", index=False)
df_valvulas.to_excel("data_valvulas.xlsx", sheet_name="valvulas", index=False)
df_usuarios.to_excel("data_usuarios.xlsx", sheet_name="usuarios", index=False)
# Crear aristas entre estaciones, tanques y usuarios
aristas = []

for _ in range(num_aristas):
    # Elegir un nodo de origen: no puede ser un usuario
    origen = random.choice(estaciones + tanques + valvulas)
    
    # Elegir un nodo de destino: no puede ser una estación
    destino = random.choice(tanques + valvulas + usuarios)
    
    while destino == origen:
        destino = random.choice(tanques + valvulas + usuarios)
    
    # Capacidad de flujo en litros por segundo
    capacidad_flujo = np.random.randint(100, 5000)  # De 100 a 5000 litros/segundo
    # Longitud de la tubería en metros
    longitud_tuberia = np.random.randint(10, 1000)  # De 10 a 1000 metros
    
    aristas.append({
        'ID Origen': origen,
        'ID Destino': destino,
        'Capacidad Flujo (l/s)': capacidad_flujo,
        'Longitud Tubería (m)': longitud_tuberia
    })

# Crear DataFrame de aristas
df_aristas = pd.DataFrame(aristas)

# Mostrar el DataFrame de aristas
print("\nAristas:")
print(df_aristas)



df_aristas.to_excel("data_aristas.xlsx", sheet_name="aristas", index=False)