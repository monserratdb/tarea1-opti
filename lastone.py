import csv
import gurobipy as grb
from gurobipy import GRB_continous

def leer_datos(ruta_costos, ruta_limites, ruta_contenidos):
  """
  Lee los datos de los archivos CSV y los devuelve como estructuras de datos.

  Args:
    ruta_costos: Ruta al archivo CSV con los costos de los cereales.
    ruta_limites: Ruta al archivo CSV con los límites de nutrientes.
    ruta_contenidos: Ruta al archivo CSV con los contenidos nutricionales de los cereales.

  Returns:
    costos: Diccionario con los costos de los cereales (clave: índice, valor: costo).
    limites: Diccionario con los límites de nutrientes (clave: índice, valor: (límite inferior, límite superior)).
    contenidos: Lista de listas con los contenidos nutricionales de los cereales.
  """

  # Leer costos
  costos = {}
  with open(ruta_costos, "r") as archivo:
    reader = csv.reader(archivo)
    next(reader)  # Saltear encabezado
    for i, fila in enumerate(reader):
      costos[i + 1] = float(fila[0])

  # Leer límites
  limites = {}
  with open(ruta_limites, "r") as archivo:
    reader = csv.reader(archivo)
    next(reader)  # Saltear encabezado
    for i, fila in enumerate(reader):
      limites[i + 1] = (float(fila[0]), float(fila[1]))

  # Leer contenidos
  contenidos = []
  with open(ruta_contenidos, "r") as archivo:
    reader = csv.reader(archivo)
    next(reader)  # Saltear encabezado
    for fila in reader:
      contenidos.append([float(valor) for valor in fila])

  return costos, limites, contenidos

def optimizar_mezcla(costos, limites, contenidos):
  """
  Resuelve el modelo de optimización para la mezcla de cereales.

  Args:
    costos: Diccionario con los costos de los cereales (clave: índice, valor: costo).
    limites: Diccionario con los límites de nutrientes (clave: índice, valor: (límite inferior, límite superior)).
    contenidos: Lista de listas con los contenidos nutricionales de los cereales.

  Returns:
    modelo: Modelo de optimización lineal de Gurobi.
    x: Variables de decisión del modelo (proporciones de cereales).
    valor_optimo: Valor óptimo de la función objetivo.
  """

  # Crear modelo
  modelo = grb.Model("Mezcla de cereales")

  # Variables de decisión: x_j, proporción de cereal j en la mezcla
  x = modelo.addVars(range(1, len(costos) + 1), name="x", vtype=grb.GRB_CONTINUOUS)

  # Restricciones:
  # 1. La mezcla está compuesta únicamente por cereales.
  modelo.addConstr(grb.quicksum(x) == 1)

  # 2. Se debe cumplir una proporción mínima de nutrientes.
  for i in range(1, len(limites) + 1):
    modelo.addConstr(grb.quicksum(contenidos[i - 1][j] * x[j] for j in range(len(costos))) >= limites[i][0])

  # 3. Se debe cumplir una proporción máxima de nutrientes.
  for i in range(1, len(limites) + 1):
    modelo.addConstr(grb.quicksum(contenidos[i - 1][j] * x[j] for j in range(len(costos))) <= limites[i][1])

  # Función objetivo: minimizar el costo total
  modelo.setObjective(grb.quicksum(costos[j] * x[j] for j in range(1, len(costos) + 1)), grb.GRB_MINIMIZE)

  # Resolver el modelo
  modelo.optimize()

  # Valor óptimo
  valor_optimo = modelo.objVal

  return modelo, x, valor_optimo

def main():
  """
  Función principal que lee los datos, resuelve el modelo e imprime la solución.
  """

  # Ruta a los archivos de datos
  ruta_costos = "costos.csv"
  ruta_limites = "limites.csv"
  ruta_contenidos = "contenidos_nutricionales.csv"

  # Leer datos
  costos, limites, contenidos = leer_datos(ruta_costos, ruta_limites, ruta_contenidos)

  # Optimizar la mezcla
  modelo, x, valor_optimo = optimizar_mezcla(costos, limites, contenidos)

  # Imprimir solución
  print(f"Valor óptimo: {valor_optimo:.2f} CLP/kg")
  print("Proporciones de cereales:")
  for j in range(1, len(costos) + 1):
    print(f"Cereal {j}: {x[j].x:.2f}")

if __name__ == "__main__":
  main()
