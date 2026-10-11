"""Vista de consola: menús, input() y print(). Las reglas viven en views.py."""

from shared.herramientas import imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
import views


def pedir_entero(mensaje):
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            imprimir_error("Ingresa un número entero válido.")


def mostrar_lista(objetos):
    if not objetos:
        imprimir_info("No hay registros para mostrar.")
        return
    # Polimorfismo: cada modelo implementa etiqueta(); esta función no pregunta el tipo.
    for objeto in objetos:
        print(f" {objeto}")


def mostrar_detalle(objeto):
    if objeto is None:
        imprimir_error("Registro no encontrado.")
    else:
        print(objeto)


def pedir_datos(campos):
    datos = {}
    for campo, etiqueta in campos:
        datos[campo] = input(f"{etiqueta}: ").strip()
    return datos


def mostrar_resultado(resultado):
    exito, mensaje = resultado
    (imprimir_exito if exito else imprimir_error)(mensaje)


def menu_estudiantes():
    while True:
        imprimir_titulo("GESTIÓN DE ESTUDIANTES")
        print("1. Crear estudiante")
        print("2. Ver todos")
        print("3. Buscar")
        print("4. Ver por ID")
        print("5. Actualizar")
        print("6. Eliminar")
        print("0. Volver")
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            datos = pedir_datos([
                ("nombre", "Nombre"), ("apellido", "Apellido"),
                ("email", "Email"), ("carnet", "Carnet"),
                ("carrera", "Carrera")
            ])
            mostrar_resultado(views.crear_estudiante(datos))
        elif opcion == "2":
            mostrar_lista(views.obtener_estudiantes())
        elif opcion == "3":
            mostrar_lista(views.buscar_estudiantes(input("Buscar: ")))
        elif opcion == "4":
            mostrar_detalle(views.obtener_estudiante(pedir_entero("ID: ")))
        elif opcion == "5":
            id_registro = pedir_entero("ID del estudiante: ")
            print("Campos: nombre, apellido, email, carnet, carrera")
            campo = input("Campo a cambiar: ").strip()
            valor = input("Nuevo valor: ").strip()
            mostrar_resultado(views.actualizar_estudiante(id_registro, {campo: valor}))
        elif opcion == "6":
            mostrar_resultado(views.eliminar_estudiante(pedir_entero("ID: ")))
        elif opcion == "0":
            break
        else:
            imprimir_error("Opción no válida.")
        input("\nPresiona Enter para continuar...")


def menu_materias():
    while True:
        imprimir_titulo("GESTIÓN DE MATERIAS")
        print("1. Crear materia")
        print("2. Ver todas")
        print("3. Buscar")
        print("4. Ver por ID")
        print("5. Actualizar")
        print("6. Eliminar")
        print("7. Materias sin cupo")
        print("0. Volver")
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            datos = pedir_datos([
                ("nombre", "Nombre"), ("codigo", "Código"),
                ("creditos", "Créditos (1-10)"), ("cupos", "Cupos (0-30)")
            ])
            mostrar_resultado(views.crear_materia(datos))
        elif opcion == "2":
            mostrar_lista(views.obtener_materias())
        elif opcion == "3":
            mostrar_lista(views.buscar_materias(input("Buscar: ")))
        elif opcion == "4":
            mostrar_detalle(views.obtener_materia(pedir_entero("ID: ")))
        elif opcion == "5":
            id_registro = pedir_entero("ID de la materia: ")
            print("Campos: nombre, codigo, creditos, cupos")
            campo = input("Campo a cambiar: ").strip()
            valor = input("Nuevo valor: ").strip()
            mostrar_resultado(views.actualizar_materia(id_registro, {campo: valor}))
        elif opcion == "6":
            mostrar_resultado(views.eliminar_materia(pedir_entero("ID: ")))
        elif opcion == "7":
            mostrar_lista(views.materias_sin_cupo())
        elif opcion == "0":
            break
        else:
            imprimir_error("Opción no válida.")
        input("\nPresiona Enter para continuar...")


def menu_matriculas():
    while True:
        imprimir_titulo("GESTIÓN DE MATRÍCULAS")
        print("1. Matricular estudiante")
        print("2. Ver todas")
        print("3. Registrar nota")
        print("4. Ver certificado")
        print("5. Retirar matrícula")
        print("6. Ver matrículas por estudiante")
        print("7. Consultar promedio")
        print("0. Volver")
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            datos = pedir_datos([
                ("estudiante_id", "ID del estudiante"),
                ("materia_id", "ID de la materia"),
                ("periodo", "Periodo (ej. 2026-1)")
            ])
            mostrar_resultado(views.crear_matricula(datos))
        elif opcion == "2":
            mostrar_lista(views.obtener_matriculas())
        elif opcion == "3":
            id_registro = pedir_entero("ID de matrícula: ")
            nota = input("Nota (0-20): ").strip()
            mostrar_resultado(views.registrar_nota(id_registro, nota))
        elif opcion == "4":
            id_registro = pedir_entero("ID del estudiante: ")
            certificado = views.certificado(id_registro)
            print(certificado if certificado else "Estudiante no encontrado.")
        elif opcion == "5":
            mostrar_resultado(views.retirar_matricula(pedir_entero("ID de matrícula: ")))
        elif opcion == "6":
            agrupadas = views.matriculas_por_estudiante()
            if not agrupadas:
                imprimir_info("No hay matrículas registradas.")
            for estudiante_id, matriculas in agrupadas.items():
                print(f"\nEstudiante ID {estudiante_id}:")
                mostrar_lista(matriculas)
        elif opcion == "7":
            id_estudiante = pedir_entero("ID del estudiante: ")
            print(f"Promedio: {views.promedio_de_estudiante(id_estudiante):.2f}")
        elif opcion == "0":
            break
        else:
            imprimir_error("Opción no válida.")
        input("\nPresiona Enter para continuar...")


def mostrar_resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")
    print(f"Total de estudiantes: {len(views.obtener_estudiantes())}")
    print("Carreras distintas:", ", ".join(views.carreras()) or "Ninguna")
    print(f"Materias sin cupo: {len(views.materias_sin_cupo())}")
    print(f"Matrículas aprobadas: {len(views.matriculas_aprobadas())}")
    input("\nPresiona Enter para volver...")


def main():
    while True:
        imprimir_titulo("SISTEMA DE GESTIÓN ACADÉMICA")
        print("1. Estudiantes")
        print("2. Materias")
        print("3. Matrículas")
        print("4. Resumen")
        print("0. Salir")
        opcion = input("\nOpción: ").strip()

        if opcion == "1":
            menu_estudiantes()
        elif opcion == "2":
            menu_materias()
        elif opcion == "3":
            menu_matriculas()
        elif opcion == "4":
            mostrar_resumen()
        elif opcion == "0":
            print("Hasta luego.")
            break
        else:
            imprimir_error("Opción no válida.")
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
