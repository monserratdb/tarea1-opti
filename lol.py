import gurobipy as gp
from gurobipy import GRB
import csv

def read_csv(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            data.append([float(value) for value in row])
    return data

def main():
    # Leer datos de los archivos CSV
    costos = read_csv('costos.csv')
    limites = read_csv('limites.csv')
    contenidos_nutricionales = read_csv('contenidos_nutricionales.csv')

    # Crear el modelo
    model = gp.Model("Optimizacion_Gallos")

    # Variables
    num_cereales = len(costos)
    x = {}
    for j in range(num_cereales):
        x[j] = model.addVar(vtype=GRB.CONTINUOUS, name=f"x_{j}")

    # Función Objetivo
    model.setObjective(gp.quicksum(costos[j][0] * x[j] for j in range(num_cereales)), GRB.MINIMIZE)

    # Restricciones
    num_nutrientes = len(limites)
    for i in range(num_nutrientes):
        model.addConstr(gp.quicksum(contenidos_nutricionales[j][i] * x[j] for j in range(num_cereales)) >= limites[i][0])
        model.addConstr(gp.quicksum(contenidos_nutricionales[j][i] * x[j] for j in range(num_cereales)) <= limites[i][1])

    # Optimizar el modelo
    model.optimize()

    # Imprimir resultados
    if model.status == GRB.OPTIMAL:
        print(f"Valor óptimo: {model.objVal} CLP por kg")
        print("Proporciones óptimas de cereales:")
        for j in range(num_cereales):
            print(f"Cereal {j + 1}: {x[j].x * 100:.2f}%")

if __name__ == "__main__":
    main()
