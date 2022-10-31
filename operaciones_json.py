"""Operaciones que se realizan sobre la base de datos (archivos JSON)."""

import json
from mecanismos_criptograficos import *


def cargarJSON(nombre_json: str) -> list:
    try:
        with open(nombre_json, 'r') as archivo:
            datos_archivo = json.load(archivo)
    except FileNotFoundError:
        datos_archivo = []

    return datos_archivo


def guardarRegistro(usuario, nombre, apellidos, email, telefono, password) -> bool:
    """Función que guarda los datos de registro en el JSON."""
                        
    clave = generarClave()
    salt = generadorSALT()
                        
    datos = {
        'usuario': usuario,
        'nombre': nombre,
        'apellidos': apellidos,
        # LA CLAVE NO SE GUARDA AQUÍ REALMENTE:
        # https://i.blogs.es/d36df6/criptografia-simetrica-20-copia-/1366_2000.png
        'clave': clave,
        'email': cifrarAES128(email, clave),
        'telefono': cifrarAES128(telefono, clave),
        'salt': salt,
        'password': crearFuncionResumenSHA256(salt + password),
        'dinero': cifrarAES128(str(0), clave),
        'productos': []
    }

    registros = cargarJSON("registros.json")
    registros.append(datos)
    guardarDatos(registros, "registros.json")


def guardarDatos(datos: list, archivo: str) -> bool:
    try:
        with open(archivo, 'w') as archivo_json:
            json.dump(datos, archivo_json, indent=4)
            return True
    except FileNotFoundError:
        print("[ERROR] El archivo JSON no existe.")

    return False


def buscarUsuario(usuario: str, archivo: str) -> bool:
    """Función que comprueba si un usuario está registrado en el JSON"""
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            return registro

    return False


def guardarLicencia(usuario: str, tipo: str, precio: str, licencia: str, archivo: str) -> bool:

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            # APLICAR CIFRADO AES 128 A LA LICENCIA --> cifrarAES128(licencia)
            lic = {'usuario': usuario,
                   'tipo': tipo,
                   'precio': float(precio),
                   'licencia': cifrarAES128(licencia, registro["clave"])}
            registro["productos"].append(lic)
            datos.append(registro)
            if guardarDatos(datos, "registros.json"):
                return True

    return False


def obtenerProductos(usuario: str, archivo: str):
    productos = []

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] != usuario:
            for producto in registro["productos"]:
                productos.append(producto)

    return productos


def obtenerMisProductos(usuario: str, archivo: str):
    productos = []

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            for producto in registro["productos"]:
                productos.append(producto)

    return productos


def comprarProducto(comprador:str, vendedor: str, tipo: str, precio: float, archivo: str) -> bool:
    datos = cargarJSON(archivo)
    # Elimina el producto comprado y suma el dinero al vendedor.
    for registro in datos:
        if registro["usuario"] == vendedor:
            for producto in registro["productos"]:
                if producto["tipo"] == tipo and producto["precio"] == precio:
                    datos.remove(registro)
                    registro["productos"].remove(producto)
                    dinero_registro = float(descifrarAES128(registro["dinero"], registro["clave"]))
                    dinero_registro += precio
                    dinero = cifrarAES128(str(dinero_registro), registro["clave"])
                    registro["dinero"] = dinero
                    datos.append(registro)
                    
                    # Resta el dinero al comprador.
                    for registro in datos:
                        if registro["usuario"] == comprador:
                            datos.remove(registro)
                            dinero_registro = float(descifrarAES128(registro["dinero"], registro["clave"]))
                            dinero_registro -= producto["precio"]
                            dinero = cifrarAES128(str(dinero_registro), registro["clave"])
                            registro["dinero"] = dinero
                            datos.append(registro)
                            if guardarDatos(datos, "registros.json"):
                                return True

    return False


def ingresoDinero(usuario: str, dinero: float, archivo: str):
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            dinero_descifrado = float(descifrarAES128(registro["dinero"], registro["clave"]))
            dinero_descifrado += dinero
            dinero_cifrado = cifrarAES128(str(dinero_descifrado), registro["clave"])
            registro["dinero"] = dinero_cifrado
            datos.append(registro)
            if guardarDatos(datos, "registros.json"):
                return True
    
    return False


def eliminarProducto(usuario: str, producto, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            for producto_registrado in registro["productos"]:
                if producto_registrado["tipo"] == producto["tipo"] and producto_registrado["precio"] == producto["precio"]:
                    datos.remove(registro)
                    registro["productos"].remove(producto_registrado)
                    datos.append(registro)

    if guardarDatos(datos, "registros.json"):
        return True

    return False
    

def verDinero(usuario: str, archivo: str) -> float:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            dinero = descifrarAES128(registro["dinero"], registro["clave"])

    return float(dinero)


def cambiarUsuario(usuario, nuevo_usuario, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            registro["usuario"] = nuevo_usuario
            datos.append(registro)

            for producto in registro["productos"]:
                producto["usuario"] = nuevo_usuario
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False

    
def cambiarNombre(usuario, nuevo_nombre, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            registro["nombre"] = nuevo_nombre
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False

    
def cambiarApellidos(usuario, nuevo_apellido, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            registro["apellidos"] = nuevo_apellido
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False

    
def cambiarEmail(usuario, nuevo_email, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            email_cifrado = cifrarAES128(nuevo_email, registro["clave"])
            registro["email"] = email_cifrado
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False

    
def cambiarTelefono(usuario, nuevo_telefono, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            telefono_cifrado = cifrarAES128(nuevo_telefono, registro["clave"])
            registro["telefono"] = telefono_cifrado
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False


def cambiarPass(usuario, nueva_pass, archivo) -> bool:
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            salt = registro["salt"]
            registro["password"] = crearFuncionResumenSHA256(salt + nueva_pass)
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False


'''
# Consideramos que el dinero de una cuenta bancaria es infinito para esta aplicación.
def cargarDatosBanco(nombre, apellidos, num_tarjeta, pin):
    
    clave = generarClave()
    salt = generadorSALT()
    
    datos = {
        'nombre': usuario,
        'apellidos': nombre,
        'num_tarjeta': cifrarAES128(num_tarjeta, clave),
        'pin': crearFuncionResumenSHA256(salt + pin)
    }

    registros = cargarJSON("datos_banco.json")
    registros.append(datos)
    if guardarDatos(registros, "datos_banco.json"):
        return True

    return False
'''
