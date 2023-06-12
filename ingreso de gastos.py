import csv
from datetime import datetime

# Categorías y subcategorías
categorias = {
    'Servicios': ['Agua', 'Gas/Garrafa', 'Electricidad', 'Teléfono', 'Internet'],
    'Comida': ['Mercadería', 'Delivery'],
    'Serv. Streamer': [],
    'Transporte': ['Gasolina', 'Sube'],
    'Otra categoría': []
}

# Función registro de usuario
def registrar_usuario(nombre_usuario, contraseña):
    with open('usuarios.csv', 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([nombre_usuario, contraseña])
    print("Registro de usuario exitoso.")

# Función de autenticación de usuario
def autenticar_usuario():
    nombre_usuario = input("Ingrese su nombre de usuario: ")
    contraseña = input("Ingrese su contraseña: ")

    with open('usuarios.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        for fila in lector_csv:
            if fila[0] == nombre_usuario and fila[1] == contraseña:
                print("Autenticación exitosa.")
                return True

    print("Nombre de usuario o contraseña incorrectos.")
    return False

# Función registro de gastos
def registrar_gasto(nombre_usuario, categoria, monto):
    nombre_archivo = f"{nombre_usuario}_gastos.csv"
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(nombre_archivo, 'a', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow([fecha, categoria, monto])
    print("Gasto registrado exitosamente.")

# Función gastos por categoría
def obtener_gastos_por_categoria(nombre_usuario):
    nombre_archivo = f"{nombre_usuario}_gastos.csv"
    gastos_por_categoria = {}
    with open(nombre_archivo, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        next(lector_csv)  # Saltar la primera línea (encabezado)
        for fila in lector_csv:
            fecha, categoria, monto = fila
            monto = float(monto)
            if categoria in gastos_por_categoria:
                gastos_por_categoria[categoria] += monto
            else:
                gastos_por_categoria[categoria] = monto
    return gastos_por_categoria

# Función generar informe
def generar_informe_gastos(nombre_usuario):
    gastos_por_categoria = obtener_gastos_por_categoria(nombre_usuario)
    total_gastos = sum(gastos_por_categoria.values())

    print("Informe de gastos por categoría:")
    for categoria, monto in gastos_por_categoria.items():
        porcentaje = (monto / total_gastos) * 100
        print(f"{categoria}: ${monto:.2f} ({porcentaje:.2f}%)")
    print(f"Total de gastos: ${total_gastos:.2f}")

    # Estadísticas adicionales
    promedio_gastos = total_gastos / len(gastos_por_categoria)
    categoria_mayor_gasto = max(gastos_por_categoria, key=gastos_por_categoria.get)
    categoria_menor_gasto = min(gastos_por_categoria, key=gastos_por_categoria.get)

    print(f"\nEstadísticas adicionales:")
    print(f"Promedio de gastos por categoría: ${promedio_gastos:.2f}")
    print(f"Categoría con el mayor gasto: {categoria_mayor_gasto}")
    print(f"Categoría con el menor gasto: {categoria_menor_gasto}")

    # Exportar informe a un archivo de texto
    fecha_actual = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = f"informe_gastos_{nombre_usuario}_{fecha_actual}.txt"

    with open(nombre_archivo, 'w') as archivo_txt:
        archivo_txt.write("Informe de gastos por categoría:\n")
        for categoria, monto in gastos_por_categoria.items():
            porcentaje = (monto / total_gastos) * 100
            archivo_txt.write(f"{categoria}: ${monto:.2f} ({porcentaje:.2f}%)\n")
        archivo_txt.write(f"Total de gastos: ${total_gastos:.2f}\n")

        archivo_txt.write("\nEstadísticas adicionales:\n")
        archivo_txt.write(f"Promedio de gastos por categoría: ${promedio_gastos:.2f}\n")
        archivo_txt.write(f"Categoría con el mayor gasto: {categoria_mayor_gasto}\n")
        archivo_txt.write(f"Categoría con el menor gasto: {categoria_menor_gasto}\n")

    print(f"Informe de gastos exportado exitosamente como '{nombre_archivo}'.")

# Función borrar gastos
def borrar_gastos(nombre_usuario):
    nombre_archivo = f"{nombre_usuario}_gastos.csv"
    fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
    fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")

    gastos_borrados = 0
    with open(nombre_archivo, 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv)
        filas = list(lector_csv)
        for fila in filas:
            fecha_gasto = datetime.strptime(fila[0], "%Y-%m-%d %H:%M:%S").date()
            if fecha_inicio <= str(fecha_gasto) <= fecha_fin:
                filas.remove(fila)
                gastos_borrados += 1

    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerows(filas)

    print(f"Se han borrado {gastos_borrados} gastos.")

# Menú app
def menu(nombre_usuario):
    while True:
        print("\n--- Aplicación de Seguimiento de Gastos ---")
        print("1. Registrar un gasto")
        print("2. Generar informe de gastos")
        print("3. Borrar gastos")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Categorías disponibles:")
            for categoria, subcategorias in categorias.items():
                print(f"{categoria}: {', '.join(subcategorias)}")

            categoria = input("Ingrese la categoría del gasto: ")
            while categoria not in categorias:
                print("Categoría no válida. Intente nuevamente.")
                categoria = input("Ingrese la categoría del gasto: ")

            subcategoria = input("Ingrese la subcategoría del gasto (o presione Enter para omitir): ")
            while subcategoria not in categorias[categoria] and subcategoria != "":
                print("Subcategoría no válida. Intente nuevamente.")
                subcategoria = input("Ingrese la subcategoría del gasto (o presione Enter para omitir): ")

            monto = float(input("Ingrese el monto del gasto: "))
            registrar_gasto(nombre_usuario, f"{categoria}-{subcategoria}", monto)
        elif opcion == "2":
            generar_informe_gastos(nombre_usuario)
        elif opcion == "3":
            borrar_gastos(nombre_usuario)
        elif opcion == "4":
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Menú principal
def menu_principal():
    print("--- Aplicación de Seguimiento de Gastos ---")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        autenticado = autenticar_usuario()
        if autenticado:
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            menu(nombre_usuario)
    elif opcion == "2":
        nombre_usuario = input("Ingrese un nombre de usuario: ")
        contraseña = input("Ingrese una contraseña: ")
        registrar_usuario(nombre_usuario, contraseña)
    elif opcion == "3":
        return
    else:
        print("Opción inválida. Intente nuevamente.")
        menu_principal()

# Ejecutar aplicación
menu_principal()
