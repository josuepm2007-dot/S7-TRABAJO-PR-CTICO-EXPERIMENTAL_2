"""Controladores y reglas del negocio. Este archivo no usa print() ni input()."""

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

gestor_estudiantes = GestorJSON("data/estudiantes.json")
gestor_materias = GestorJSON("data/materias.json")
gestor_matriculas = GestorJSON("data/matriculas.json")


# Funciones genéricas: sirven para cualquier modelo que implemente a_diccionario.
def leer_objetos(gestor, clase):
    return [clase.desde_diccionario(d) for d in gestor.leer()]


def obtener_por_id(objetos, id_registro):
    try:
        id_registro = int(id_registro)
    except (TypeError, ValueError):
        return None
    for objeto in objetos:
        if objeto.id == id_registro:
            return objeto
    return None


def buscar(objetos, termino, campos):
    termino = str(termino).strip().casefold()
    if not termino:
        return []
    encontrados = []
    # La tupla fija declara qué campos se pueden buscar para cada entidad.
    for objeto in objetos:
        if any(termino in str(getattr(objeto, campo, "")).casefold() for campo in campos):
            encontrados.append(objeto)
    return encontrados


def siguiente_id(objetos):
    return max((objeto.id for objeto in objetos), default=0) + 1


def guardar_nuevo(gestor, objetos, objeto):
    objetos.append(objeto)
    return reemplazar(gestor, objetos)


def reemplazar(gestor, objetos):
    return gestor.guardar([objeto.a_diccionario() for objeto in objetos])


def eliminar(gestor, objetos, id_registro):
    objeto = obtener_por_id(objetos, id_registro)
    if objeto is None:
        return False, f"No existe el registro con id {id_registro}"
    objetos.remove(objeto)
    reemplazar(gestor, objetos)
    return True, f"Registro {id_registro} eliminado"


def ids_registrados(objetos, excepto_id=None):
    # Conjunto: permite comprobar si un ID ya existe sin recorrer la lista cada vez.
    return {objeto.id for objeto in objetos if objeto.id != excepto_id}


def indice_por_id(objetos):
    # Diccionario índice {id: objeto}; permite cruzar relaciones por ID.
    return {objeto.id: objeto for objeto in objetos}


# ---------------------------------------------------------------------
# ESTUDIANTES
# ---------------------------------------------------------------------
def obtener_estudiantes():
    return leer_objetos(gestor_estudiantes, Estudiante)


def obtener_estudiante(id_estudiante):
    return obtener_por_id(obtener_estudiantes(), id_estudiante)


def carnets_registrados(excepto_id=None):
    # Set: detectar carnets duplicados con una consulta de pertenencia rápida.
    return {
        r["carnet"].strip().upper()
        for r in gestor_estudiantes.leer()
        if r["id"] != excepto_id
    }


def validar_estudiante(datos, id_actual=None):
    if id_actual is None:
        for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
            if not str(datos.get(campo, "")).strip():
                return f"El campo {campo} es obligatorio"

    if "email" in datos:
        email = str(datos["email"]).strip().lower()
        if not es_email_valido(email):
            return "El email no tiene un formato válido"
        usados = {
            r["email"].strip().lower()
            for r in gestor_estudiantes.leer()
            if r["id"] != id_actual
        }
        if email in usados:
            return "Ese email ya está registrado"

    if "carnet" in datos:
        carnet = str(datos["carnet"]).strip().upper()
        if carnet in carnets_registrados(id_actual):
            return "Ese carnet ya está registrado"
    return None


def crear_estudiante(datos):
    error = validar_estudiante(datos)
    if error:
        return False, error
    estudiante = Estudiante(
        siguiente_id(obtener_estudiantes()),
        str(datos["nombre"]).strip().title(),
        str(datos["apellido"]).strip().title(),
        str(datos["email"]).strip().lower(),
        str(datos["carnet"]).strip().upper(),
        str(datos["carrera"]).strip().title(),
    )
    estudiantes = obtener_estudiantes()
    guardar_nuevo(gestor_estudiantes, estudiantes, estudiante)
    return True, f"Estudiante creado: {estudiante.etiqueta()}"


def buscar_estudiantes(termino):
    # Tuple: campos de búsqueda fijos y no modificables por accidente.
    CAMPOS = ("nombre", "apellido", "email", "carnet", "carrera")
    return buscar(obtener_estudiantes(), termino, CAMPOS)


def actualizar_estudiante(id_estudiante, cambios):
    estudiantes = obtener_estudiantes()
    estudiante = obtener_por_id(estudiantes, id_estudiante)
    if estudiante is None:
        return False, f"No existe el estudiante {id_estudiante}"
    if not cambios:
        return False, "No se indicó ningún cambio"
    permitidos = {"nombre", "apellido", "email", "carnet", "carrera"}
    desconocidos = set(cambios) - permitidos
    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
    error = validar_estudiante(cambios, int(id_estudiante))
    if error:
        return False, error
    for campo, valor in cambios.items():
        valor = str(valor).strip()
        if campo in ("nombre", "apellido", "carrera"):
            valor = valor.title()
        elif campo == "email":
            valor = valor.lower()
        elif campo == "carnet":
            valor = valor.upper()
        setattr(estudiante, campo, valor)
    reemplazar(gestor_estudiantes, estudiantes)
    return True, f"Estudiante {id_estudiante} actualizado"


def eliminar_estudiante(id_estudiante):
    # No se permite borrar un estudiante que conserve matrículas.
    if any(m.estudiante_id == int(id_estudiante) for m in obtener_matriculas()):
        return False, "No se puede eliminar: el estudiante tiene matrículas registradas"
    estudiantes = obtener_estudiantes()
    estudiante = obtener_por_id(estudiantes, id_estudiante)
    if estudiante is None:
        return False, f"No existe el estudiante {id_estudiante}"
    estudiantes.remove(estudiante)
    reemplazar(gestor_estudiantes, estudiantes)
    return True, f"Estudiante {id_estudiante} eliminado"


def carreras():
    # Set para obtener carreras distintas; sorted() las presenta ordenadas.
    return sorted({e.carrera for e in obtener_estudiantes() if e.carrera})


# ---------------------------------------------------------------------
# MATERIAS
# ---------------------------------------------------------------------
def obtener_materias():
    return leer_objetos(gestor_materias, Materia)


def obtener_materia(id_materia):
    return obtener_por_id(obtener_materias(), id_materia)


def codigos_registrados(excepto_id=None):
    # Set: los códigos de materia deben ser únicos.
    return {
        r["codigo"].strip().upper()
        for r in gestor_materias.leer()
        if r["id"] != excepto_id
    }


def validar_materia(datos, id_actual=None):
    if id_actual is None:
        for campo in ("nombre", "codigo", "creditos", "cupos"):
            if not str(datos.get(campo, "")).strip():
                return f"El campo {campo} es obligatorio"

    if "codigo" in datos:
        codigo = str(datos["codigo"]).strip().upper()
        if not codigo:
            return "El código es obligatorio"
        if codigo in codigos_registrados(id_actual):
            return "Ese código ya está registrado"

    if "nombre" in datos and not str(datos["nombre"]).strip():
        return "El nombre es obligatorio"

    if "creditos" in datos:
        try:
            creditos = int(datos["creditos"])
        except (TypeError, ValueError):
            return "Los créditos deben ser un número entero"
        if not 1 <= creditos <= 10:
            return "Los créditos deben estar entre 1 y 10"

    if "cupos" in datos:
        try:
            cupos = int(datos["cupos"])
        except (TypeError, ValueError):
            return "Los cupos deben ser un número entero"
        if not 0 <= cupos <= Materia.CUPOS_MAXIMOS:
            return f"Los cupos deben estar entre 0 y {Materia.CUPOS_MAXIMOS}"
    return None


def crear_materia(datos):
    error = validar_materia(datos)
    if error:
        return False, error
    materia = Materia(
        siguiente_id(obtener_materias()),
        str(datos["nombre"]).strip().title(),
        str(datos["codigo"]).strip().upper(),
        int(datos["creditos"]),
        int(datos["cupos"]),
    )
    guardar_nuevo(gestor_materias, obtener_materias(), materia)
    return True, f"Materia creada: {materia.etiqueta()}"


def obtener_materias_lista():
    return obtener_materias()


def buscar_materias(termino):
    CAMPOS = ("nombre", "codigo")
    return buscar(obtener_materias(), termino, CAMPOS)


def actualizar_materia(id_materia, cambios):
    materias = obtener_materias()
    materia = obtener_por_id(materias, id_materia)
    if materia is None:
        return False, f"No existe la materia {id_materia}"
    if not cambios:
        return False, "No se indicó ningún cambio"
    permitidos = {"nombre", "codigo", "creditos", "cupos"}
    desconocidos = set(cambios) - permitidos
    if desconocidos:
        return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"
    error = validar_materia(cambios, int(id_materia))
    if error:
        return False, error
    for campo, valor in cambios.items():
        if campo == "nombre":
            valor = str(valor).strip().title()
        elif campo == "codigo":
            valor = str(valor).strip().upper()
        else:
            valor = int(valor)
        setattr(materia, campo, valor)
    reemplazar(gestor_materias, materias)
    return True, f"Materia {id_materia} actualizada"


def eliminar_materia(id_materia):
    if any(m.materia_id == int(id_materia) for m in obtener_matriculas()):
        return False, "No se puede eliminar: la materia tiene matrículas registradas"
    materias = obtener_materias()
    materia = obtener_por_id(materias, id_materia)
    if materia is None:
        return False, f"No existe la materia {id_materia}"
    materias.remove(materia)
    reemplazar(gestor_materias, materias)
    return True, f"Materia {id_materia} eliminada"


def materias_sin_cupo():
    return [materia for materia in obtener_materias() if not materia.hay_cupo()]


# ---------------------------------------------------------------------
# MATRÍCULAS
# ---------------------------------------------------------------------
def obtener_matriculas():
    return leer_objetos(gestor_matriculas, Matricula)


def obtener_matricula(id_matricula):
    return obtener_por_id(obtener_matriculas(), id_matricula)


def crear_matricula(datos):
    # Las funciones devuelven una tupla (exito, mensaje): separa el resultado lógico
    # del texto que la capa de presentación mostrará al usuario.
    try:
        estudiante_id = int(datos["estudiante_id"])
        materia_id = int(datos["materia_id"])
    except (KeyError, TypeError, ValueError):
        return False, "El ID del estudiante y el ID de la materia son obligatorios y numéricos"

    periodo = str(datos.get("periodo", "")).strip()
    if not periodo:
        return False, "El periodo es obligatorio"
    if obtener_estudiante(estudiante_id) is None:
        return False, f"No existe el estudiante {estudiante_id}"
    materias = obtener_materias()
    materia = obtener_por_id(materias, materia_id)
    if materia is None:
        return False, f"No existe la materia {materia_id}"
    # Primero se comprueba la combinación estudiante-materia-periodo para dar el error específico.
    for existente in obtener_matriculas():
        if (
            existente.estudiante_id == estudiante_id
            and existente.materia_id == materia_id
            and existente.periodo.casefold() == periodo.casefold()
        ):
            return False, "El estudiante ya está matriculado en esa materia durante ese periodo"

    if not materia.hay_cupo():
        return False, "La materia no tiene cupos disponibles"

    matricula = Matricula(
        siguiente_id(obtener_matriculas()), estudiante_id, materia_id, periodo, 0
    )
    materia.ocupar_cupo()
    matriculas = obtener_matriculas()
    guardar_nuevo(gestor_matriculas, matriculas, matricula)
    reemplazar(gestor_materias, materias)
    return True, f"Matrícula creada: {matricula.etiqueta()}"


def registrar_nota(id_matricula, nota):
    matriculas = obtener_matriculas()
    matricula = obtener_por_id(matriculas, id_matricula)
    if matricula is None:
        return False, f"No existe la matrícula {id_matricula}"
    if not Materia.es_nota_valida(nota):
        return False, "La nota debe ser un número entre 0 y 20"
    matricula.nota = float(nota)
    reemplazar(gestor_matriculas, matriculas)
    return True, f"Nota registrada: {matricula.nota:.2f} · {matricula.estado()}"


def retirar_matricula(id_matricula):
    matriculas = obtener_matriculas()
    matricula = obtener_por_id(matriculas, id_matricula)
    if matricula is None:
        return False, f"No existe la matrícula {id_matricula}"
    materias = obtener_materias()
    materia = obtener_por_id(materias, matricula.materia_id)
    if materia is not None:
        materia.liberar_cupo()
        reemplazar(gestor_materias, materias)
    matriculas.remove(matricula)
    reemplazar(gestor_matriculas, matriculas)
    return True, f"Matrícula {id_matricula} retirada y cupo liberado"


def certificado(id_estudiante):
    estudiante = obtener_estudiante(id_estudiante)
    if estudiante is None:
        return None
    # Índices por ID evitan búsquedas repetidas al cruzar estudiante, materia y matrícula.
    estudiantes_idx = indice_por_id(obtener_estudiantes())
    materias_idx = indice_por_id(obtener_materias())
    if estudiante.id not in estudiantes_idx:
        return None
    lineas = [
        f"CERTIFICADO ACADÉMICO · {estudiante.nombre_completo()}",
        f"Carnet: {estudiante.carnet}",
        f"Carrera: {estudiante.carrera}",
        "-" * 55,
    ]
    propias = [m for m in obtener_matriculas() if m.estudiante_id == estudiante.id]
    if not propias:
        lineas.append("No existen matrículas registradas.")
    for matricula in propias:
        materia = materias_idx.get(matricula.materia_id)
        if materia is None:
            nombre = "Materia no disponible"
            codigo = "N/A"
            creditos = "N/A"
        else:
            nombre, codigo, creditos = materia.nombre, materia.codigo, materia.creditos
        lineas.extend([
            f"Periodo: {matricula.periodo}",
            f"Materia: {nombre} ({codigo}) · {creditos} créditos",
            f"Nota: {matricula.nota:.2f}",
            f"Estado: {matricula.estado()}",
            "-" * 55,
        ])
    return "\n".join(lineas)


def matriculas_por_estudiante():
    """Diccionario de listas: cada estudiante apunta a sus matrículas."""
    agrupadas = {}
    for matricula in obtener_matriculas():
        # setdefault crea la lista la primera vez que aparece ese estudiante.
        agrupadas.setdefault(matricula.estudiante_id, []).append(matricula)
    return agrupadas


def promedio_de_estudiante(id_estudiante):
    notas = [
        m.nota for m in obtener_matriculas()
        if m.estudiante_id == int(id_estudiante)
    ]
    return round(sum(notas) / len(notas), 2) if notas else 0.0


def matriculas_aprobadas():
    return [m for m in obtener_matriculas() if m.esta_aprobada()]
