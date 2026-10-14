"""Soluciones de los 10 ejercicios de la sección 15 de la guía.

Los ejercicios 6 a 10 pertenecen al proyecto de ventas usado como ejemplo en la guía;
se resuelven aquí de forma independiente para no mezclar esas clases con el sistema académico.
"""

# ---------------------------------------------------------------------
# EJERCICIO 1 · Quitar duplicados conservando el orden
# ---------------------------------------------------------------------
def ejercicio_1():
    ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
    resultado = list(dict.fromkeys(ciudades))
    print(resultado)  # ['Quito', 'Guayaquil', 'Cuenca']


# ---------------------------------------------------------------------
# EJERCICIO 2 · Contar con un diccionario
# ---------------------------------------------------------------------
def ejercicio_2():
    ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]
    conteo = {}
    for ciudad in ciudades:
        conteo[ciudad] = conteo.get(ciudad, 0) + 1
    print(conteo)


# ---------------------------------------------------------------------
# EJERCICIO 3 · Conjuntos en acción
# ---------------------------------------------------------------------
def ejercicio_3():
    inscritos_matematica = {"Ana", "Luis", "Sol", "Marco"}
    inscritos_ingles = {"Luis", "Marco", "Ruth"}
    print("En ambas:", inscritos_matematica & inscritos_ingles)
    print("Solo matemática:", inscritos_matematica - inscritos_ingles)
    print("Total de estudiantes distintos:", len(inscritos_matematica | inscritos_ingles))


# ---------------------------------------------------------------------
# EJERCICIO 4 · De lista de diccionarios a índice
# ---------------------------------------------------------------------
def ejercicio_4():
    clientes = [{"id": 1, "nombre": "Ana"}, {"id": 2, "nombre": "Luis"}]
    # Diccionario índice: permite consultar directamente el cliente usando su ID.
    indice = {cliente["id"]: cliente for cliente in clientes}
    print(indice[2]["nombre"])


# ---------------------------------------------------------------------
# EJERCICIO 5 · Tuplas como registros inmutables
# ---------------------------------------------------------------------
def ejercicio_5():
    ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
    mes_mayor, monto_mayor = max(ventas, key=lambda venta: venta[1])
    total = sum(monto for mes, monto in ventas)
    print("Mes con mayor venta:", mes_mayor, monto_mayor)
    print("Total vendido:", total)


# ---------------------------------------------------------------------
# EJERCICIO 6 · clientes_por_ciudad()
# ---------------------------------------------------------------------
def clientes_por_ciudad(clientes):
    """Devuelve ciudad -> lista de nombres de clientes de esa ciudad."""
    resultado = {}
    for cliente in clientes:
        # setdefault crea la lista de esa ciudad solo cuando aparece por primera vez.
        resultado.setdefault(cliente["ciudad"], []).append(cliente["nombre"])
    return resultado


def ejercicio_6():
    clientes = [
        {"id": 1, "nombre": "Ana", "ciudad": "Guayaquil"},
        {"id": 2, "nombre": "Luis", "ciudad": "Guayaquil"},
        {"id": 3, "nombre": "Sol", "ciudad": "Quito"},
    ]
    print(clientes_por_ciudad(clientes))


# ---------------------------------------------------------------------
# EJERCICIO 7 · ¿Instancia, de clase o estático?
# ---------------------------------------------------------------------
def ejercicio_7():
    respuestas = {
        "a) Calcular el total de una venta": "método de instancia: usa los datos de esa venta",
        "b) Crear Producto desde un diccionario": "método de clase: recibe cls y construye una instancia",
        "c) Saber si un precio es válido": "método estático: valida el valor sin necesitar un objeto",
        "d) Saber si un producto tiene stock bajo": "método de instancia: consulta el stock de ese producto",
        "e) Calcular el IVA de cualquier monto": "método estático: opera con el monto recibido",
    }
    for pregunta, respuesta in respuestas.items():
        print(pregunta, "->", respuesta)


# ---------------------------------------------------------------------
# EJERCICIO 8 · Proveedor hereda de Persona
# ---------------------------------------------------------------------
class Persona:
    """Versión mínima de Persona para resolver este ejercicio por separado."""
    def __init__(self, id_registro, nombre, apellido, email):
        self.id = int(id_registro)
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def a_diccionario(self):
        return {"id": self.id, "nombre": self.nombre,
                "apellido": self.apellido, "email": self.email}

    def etiqueta(self):
        return f"{self.nombre} {self.apellido}"


class Proveedor(Persona):
    def __init__(self, id_registro, nombre, apellido, email, ruc, empresa):
        super().__init__(id_registro, nombre, apellido, email)
        self.ruc = ruc
        self.empresa = empresa

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos["ruc"] = self.ruc
        datos["empresa"] = self.empresa
        return datos

    def etiqueta(self):
        return f"{super().etiqueta()} · {self.empresa} · RUC {self.ruc}"


def ejercicio_8():
    proveedor = Proveedor(1, "Mario", "López", "mario@empresa.com", "0999999999001", "Suministros ML")
    print(proveedor.a_diccionario())
    print(proveedor.etiqueta())


# ---------------------------------------------------------------------
# EJERCICIO 9 · Polimorfismo sin if de tipo
# ---------------------------------------------------------------------
class ClienteEjemplo:
    def __init__(self, nombre, apellido, ciudad):
        self.nombre, self.apellido, self.ciudad = nombre, apellido, ciudad

    def describir(self):
        return f"{self.nombre} {self.apellido} de {self.ciudad}"


class ProductoEjemplo:
    def __init__(self, nombre, precio):
        self.nombre, self.precio = nombre, precio

    def describir(self):
        return f"{self.nombre} a ${self.precio}"


class VentaEjemplo:
    def __init__(self, cantidad):
        self.cantidad = cantidad

    def describir(self):
        return f"venta de {self.cantidad} unidades"


def describir(objeto):
    # Polimorfismo: cada clase sabe describirse; no se pregunta por el tipo de objeto.
    return objeto.describir()


def ejercicio_9():
    objetos = [
        ClienteEjemplo("Ana", "Pérez", "Guayaquil"),
        ProductoEjemplo("Teclado", 15.5),
        VentaEjemplo(3),
    ]
    for objeto in objetos:
        print(describir(objeto))


# ---------------------------------------------------------------------
# EJERCICIO 10 · Atributo estático y precio mayorista
# ---------------------------------------------------------------------
class ProductoEjemploMayorista:
    DESCUENTO_MAYORISTA = 0.10

    @staticmethod
    def precio_mayorista(precio, cantidad):
        precio = float(precio)
        cantidad = int(cantidad)
        if cantidad >= 12:
            return precio * (1 - ProductoEjemploMayorista.DESCUENTO_MAYORISTA)
        return precio


def ejercicio_10():
    precio = 20.0
    cantidad = 12
    precio_final = ProductoEjemploMayorista.precio_mayorista(precio, cantidad)
    print(f"Precio unitario: ${precio:.2f}")
    print(f"Cantidad: {cantidad}")
    print(f"Precio mayorista unitario: ${precio_final:.2f}")


if __name__ == "__main__":
    for numero in range(1, 11):
        print(f"\n{'=' * 12} EJERCICIO {numero} {'=' * 12}")
        globals()[f"ejercicio_{numero}"]()
