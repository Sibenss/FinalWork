import csv
from datetime import datetime

# funcion registro de gastos
def registrar_gasto(categoria, monto):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('gastos.csv', 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([fecha, categoria, monto])
    print("Gasto registrado exitosamente.")

# funcion gastos por categoria
def obtener_gastos_por_categoria():
    gastos_por_categoria = {}
    with open('gastos.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            categoria = fila[1]
            monto = float(fila[2])
            if categoria in gastos_por_categoria:
                gastos_por_categoria[categoria] += monto
            else:
                gastos_por_categoria[categoria] = monto
    return gastos_por_categoria

# funcion generar informe
def generar_informe_gastos():
    gastos_por_categoria = obtener_gastos_por_categoria()
    total_gastos = sum(gastos_por_categoria.values())

    print("Informe de gastos por categoría:")
    for categoria, monto in gastos_por_categoria.items():
        porcentaje = (monto / total_gastos) * 100
        print(f"{categoria}: ${monto:.2f} ({porcentaje:.2f}%)")
    print(f"Total de gastos: ${total_gastos:.2f}")
    
# Función borrar gastos
def borrar_gastos():
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

    gastos_borrados = 0
    with open('gastos.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        filas = list(lector_csv)
        for fila in filas:
            fecha_gasto = datetime.strptime(fila[0], "%Y-%m-%d %H:%M:%S").date()
            if fecha_inicio <= str(fecha_gasto) <= fecha_fin:
                filas.remove(fila)
                gastos_borrados += 1

    with open('gastos.csv', 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(filas)

    print(f"Se han borrado {gastos_borrados} gastos.")

# menu app
def menu():
    while True:
        print("\n--- Aplicación de Seguimiento de Gastos ---")
        print("1. Registrar un gasto")
        print("2. Generar informe de gastos")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            categoria = input("Ingrese la categoría del gasto: ")
            monto = float(input("Ingrese el monto del gasto: "))
            registrar_gasto(categoria, monto)
        elif opcion == "2":
            generar_informe_gastos()
        elif opcion == "3":
            break
        else:
            print("Opción inválida. Intente nuevamente.")


# ejecutar app
menu()
