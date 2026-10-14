from pathlib import Path

content = '''import json
import os


class GestorJSON:
    """Clase encargada de leer y escribir archivos JSON."""

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)

        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)

    def leer(self):
        """Lee el JSON y devuelve una lista. Si no existe o falla, devuelve []."""
        if not os.path.exists(self.ruta):
            return []

        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            return datos if isinstance(datos, list) else []

        except (json.JSONDecodeError, OSError):
            return []

    def guardar(self, datos):
        """Guarda una lista en el archivo JSON."""
        try:
            carpeta = os.path.dirname(self.ruta)

            if carpeta:
                os.makedirs(carpeta, exist_ok=True)

            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)

            return True

        except (TypeError, OSError):
            return False

    def agregar(self, dato):
        """Agrega un registro al final de la lista."""
        datos = self.leer()
        datos.append(dato)
        return self.guardar(datos)

    def buscar(self, campo, valor):
        """Devuelve una lista con los registros cuyo campo coincide con valor."""
        datos = self.leer()
        encontrados = []

        for registro in datos:
            if isinstance(registro, dict) and registro.get(campo) == valor:
                encontrados.append(registro)

        return encontrados

    def obtener_por_id(self, id_registro):
        """Devuelve el primer registro con ese ID o None si no existe."""
        datos = self.leer()

        for registro in datos:
            if isinstance(registro, dict) and str(registro.get("id")) == str(id_registro):
                return registro

        return None

    def existe(self, id_registro):
        """Devuelve True si existe un registro con ese ID."""
        return self.obtener_por_id(id_registro) is not None

    def actualizar(self, id_registro, nuevos_datos):
        """Actualiza los campos de un registro existente. Devuelve True si lo actualiza."""
        if not isinstance(nuevos_datos, dict):
            return False

        datos = self.leer()

        for registro in datos:
            if isinstance(registro, dict) and str(registro.get("id")) == str(id_registro):
                registro.update(nuevos_datos)
                return self.guardar(datos)

        return False

    def eliminar(self, id_registro):
        """Elimina un registro por ID. Devuelve True si lo encontró y guardó el cambio."""
        datos = self.leer()
        datos_filtrados = [
            registro
            for registro in datos
            if not (
                isinstance(registro, dict)
                and str(registro.get("id")) == str(id_registro)
            )
        ]

        if len(datos_filtrados) == len(datos):
            return False

        return self.guardar(datos_filtrados)

    def contar(self):
        """Devuelve la cantidad de registros guardados."""
        return len(self.leer())

    def vaciar(self):
        """Reemplaza el contenido del archivo por una lista vacía."""
        return self.guardar([])


# ============================================================
# EJEMPLOS DE USO (COMENTADOS)
# Descomenta y adapta estas líneas solo cuando quieras probar.
# No se ejecutan mientras permanezcan comentadas.
# ============================================================

# gestor = GestorJSON("data/estudiantes.json")
#
# # Leer todos los registros
# estudiantes = gestor.leer()
# print(estudiantes)
#
# # Guardar una lista completa
# gestor.guardar([
#     {"id": 1, "nombre": "Josue", "edad": 19},
#     {"id": 2, "nombre": "Carlos", "edad": 20}
# ])
#
# # Agregar un registro
# gestor.agregar({"id": 3, "nombre": "Ana", "edad": 18})
#
# # Buscar por un campo (por ejemplo, nombre)
# encontrados = gestor.buscar("nombre", "Josue")
# print(encontrados)
#
# # Obtener un registro por ID
# estudiante = gestor.obtener_por_id(1)
# print(estudiante)
#
# # Comprobar si existe un ID
# print(gestor.existe(2))
#
# # Actualizar campos de un registro existente
# gestor.actualizar(1, {"nombre": "Josue Steven", "edad": 20})
#
# # Eliminar un registro por ID
# gestor.eliminar(2)
#
# # Contar registros
# print(gestor.contar())
#
# # Vaciar el archivo (¡esto elimina todos los registros guardados!)
# # gestor.vaciar()
'''
path = Path("/mnt/data/json_manager.py")
path.write_text(content, encoding="utf-8")
print(f"Archivo creado: {path} | {path.stat().st_size} bytes")
