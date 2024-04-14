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
archivo_costos = 'costos.csv'
archivo_limites = 'limites.csv'
archivo_contenidos = 'contenidos_nutricionales.csv'

# Leer los datos de los archivos CSV
costos = read_csv(costos_file)
limites = read_csv(limites_file)
a = read_csv(contenidos_file) # Usamos a para que fuera como el enunciado

# Conjuntos J e I
J = len(costos)
I = len(limites)

# Crear el modelo con gurobi
model = gp.Model("Gallos")

# Variable y naturaleza de variables con lb
x = model.addVars(J, name="x", lb=0.0)

# Restricciones
for i in range(I):
    # Proporción mínima de nutrientes
    model.addConstr(gp.quicksum(a[i][j] * x[j] for j in range(J)) >= limites[i][0])
    #Proporción máxima de nutrientes
    model.addConstr(gp.quicksum(a[i][j] * x[j] for j in range(J)) <= limites[i][1])

# Restricción de que la suma de todas las proporciones de cereales sea igual a 1
model.addConstr(gp.quicksum(x[j] for j in range(J)) == 1)

# Función Objetivo
model.setObjective(gp.quicksum(costos[j][0] * x[j] for j in range(J)), GRB.MINIMIZE)

# Resolver el modelo
model.optimize()

# Imprimir resultados si encuentra solución
if model.status == GRB.OPTIMAL:
    print(f"Valor óptimo: {model.objVal} CLP/kg")

    print("Proporciones óptimas:")
    for j in range(J):
        print(f"Cereal {j+1}: {round(x[j].X, 3)}")

else:
    print("No se encontró una solución óptima")

