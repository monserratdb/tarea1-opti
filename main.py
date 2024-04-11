import gurobipy as gp
from gurobipy import GRB
import csv

# Función para leer los archivos CSV
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # saltar encabezado
        for row in reader:
            data.append([float(val) for val in row])
    return data

# Nombre de los archivos CSV
costos_file = 'costos.csv'
limites_file = 'limites.csv'
contenidos_file = 'contenidos_nutricionales.csv'

# Leer los datos de los archivos CSV
costos = read_csv(costos_file)
print(costos)
limites = read_csv(limites_file)
print(limites)
contenidos = read_csv(contenidos_file)
print(contenidos)

J = range(len(costos))
I = range(len(limites))

print(f"J: {list(J)}")
print(f"I: {list(I)}")
# Crear el modelo
model = gp.Model("Gallos")

# Variables
num_cereales = len(costos)
x = model.addVars(num_cereales, name="x", lb=0.0)

# Restricciones
for i in range(len(limites)):
    model.addConstr(gp.quicksum(contenidos[i][j] * x[j] for j in range(num_cereales)) >= limites[i][0])
    model.addConstr(gp.quicksum(contenidos[i][j] * x[j] for j in range(num_cereales)) <= limites[i][1])

model.addConstr(gp.quicksum(x[j] for j in range(num_cereales)) == 1)

# Función Objetivo
model.setObjective(gp.quicksum(costos[j][0] * x[j] for j in range(num_cereales)), GRB.MINIMIZE)

# Resolver el modelo
model.optimize()

# Imprimir resultados
if model.status == GRB.OPTIMAL:
    print(f"Valor óptimo: {model.objVal} CLP/kg")

    print("Proporciones óptimas:")
    for j in range(num_cereales):
        print(f"Cereal {j+1}: {x[j].X}")

else:
    print("No se encontró una solución óptima")

