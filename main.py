import gurobipy as gp
from gurobipy import GRB
import csv

def read_csv(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def main():
    # Lectura de los archivos CSV
    costos = read_csv('costos.csv')
    limites = read_csv('limites.csv')
    contenidos = read_csv('contenidos_nutricionales.csv')

    # Creación del modelo
    model = gp.Model("Optimizacion_Alimentacion")

    # Variables
    cereales = range(1, len(costos))
    x = model.addVars(cereales, name="x")

    # Restricciones
    for i in range(1, len(limites)):
        limite_inferior = float(limites[i][0])
        limite_superior = float(limites[i][1])
        model.addConstr(sum(float(contenidos[j][i-1]) * x[j] for j in cereales) >= limite_inferior, f"Limite_inferior_{i}")
        model.addConstr(sum(float(contenidos[j][i-1]) * x[j] for j in cereales) <= limite_superior, f"Limite_superior_{i}")

    # Restricción de que la mezcla esté compuesta únicamente por cereales
    model.addConstr(sum(x[j] for j in cereales) == 1, "Mezcla_compuesta_por_cereales")

    # Función Objetivo
    model.setObjective(sum(float(costos[j][0]) * x[j] for j in cereales), GRB.MINIMIZE)

    # Optimización
    model.optimize()

    # Impresión de resultados
    if model.status == GRB.OPTIMAL:
        print("Valor óptimo:", model.objVal)
        print("Proporciones óptimas de cereales:")
        for cereal in cereales:
            print(f"Cereal {cereal}: {x[cereal].x}")

if _name_ == "_main_":
    main()