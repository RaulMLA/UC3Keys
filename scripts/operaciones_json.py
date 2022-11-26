"""Operaciones que se realizan sobre la base de datos (archivos JSON)."""

import json
from scripts.mecanismos_criptograficos import *


def cargarJSON(nombre_json: str) -> list:
    """Función que carga los datos de un archivo JSON."""
    
    try:
        with open(nombre_json, 'r') as archivo:
            datos_archivo = json.load(archivo)
    except FileNotFoundError:
        datos_archivo = []

    return datos_archivo


def guardarRegistro(usuario, nombre, apellidos, email, telefono, password, clave_RSA) -> bool:
    """Función que guarda los datos de registro en el JSON."""
                        
    salt = generadorSALT()
    iv = generadorIV()
    clave = generarClave(salt, password)
    
    email_cifrado, tag_email = cifrarAES128(email, clave, iv)
    telefono_cifrado, tag_telefono = cifrarAES128(telefono, clave, iv)
    clave_cifrada, tag_clave = cifrarAES128(clave_RSA, clave, iv)
    dinero_cifrado, tag_dinero = cifrarAES128("0.0", clave, iv)
    
    datos = {
        'usuario': usuario,
        'nombre': nombre,
        'apellidos': apellidos,
        'email': email_cifrado,
        'telefono': telefono_cifrado,
        'salt': salt,
        'password': crearFuncionResumenSHA256(salt + password),
        'dinero': dinero_cifrado,
        'productos': [],
        'clave_RSA': clave_cifrada,
        'iv': iv,
        'tag_email': tag_email,
        'tag_telefono': tag_telefono,
        'tag_dinero': tag_dinero,
        'tag_clave_RSA': tag_clave
    }

    registros = cargarJSON("registros.json")
    registros.append(datos)
    guardarDatos(registros, "registros.json")


def guardarDatos(datos: list, archivo: str) -> bool:
    """Función que guarda los datos en un archivo JSON."""

    try:
        with open(archivo, 'w') as archivo_json:
            json.dump(datos, archivo_json, indent=4)
            return True
    except FileNotFoundError:
        print("[ERROR]\nEl archivo JSON no existe.")

    return False


def buscarUsuario(usuario: str, archivo: str) -> bool:
    """Función que comprueba si un usuario está registrado en el JSON"""
    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            return registro

    return False


def guardarLicencia(usuario: str, tipo: str, precio: str, licencia: str, archivo: str, password: str) -> bool:
    """Función que guarda una licencia en el JSON de un usuario."""

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)

            iv = registro["iv"]
            clave = generarClave(registro["salt"], password)
            licencia_cifrada, tag_licencia = cifrarAES128(licencia, clave, iv)

            clave_RSA = obtenerClaveRSA(usuario, password)
            string_producto = stringProducto(usuario, tipo, precio, licencia_cifrada, tag_licencia)
            hash_producto = aplicarHash(stringToBytes(string_producto))
            firma_producto = firmarRSA(hash_producto, clave_RSA)

            lic = {'usuario': usuario,
                   'tipo': tipo,
                   'precio': float(precio),
                   'licencia': licencia_cifrada,
                   'tag_licencia': tag_licencia,
                   'firma_producto': firma_producto
                  }
            
            registro["productos"].append(lic)
            datos.append(registro)
            if guardarDatos(datos, "registros.json"):
                return True

    return False


def stringProducto(usuario, tipo, precio, licencia_cifrada, tag_licencia):
    """Función que devuelve un string con los datos de un producto concatenados."""

    string_producto = usuario + tipo + str(precio) + licencia_cifrada + tag_licencia

    return string_producto


def obtenerProductos(usuario: str, archivo: str):
    """Función que devuelve los productos de los demás usuarios."""

    productos = []

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] != usuario:
            for producto in registro["productos"]:
                productos.append(producto)

    return productos


def obtenerMisProductos(usuario: str, archivo: str):
    """Función que devuelve los productos de un usuario."""

    productos = []

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            for producto in registro["productos"]:
                productos.append(producto)

    return productos


def comprarProducto(comprador:str, vendedor: str, tipo: str, precio: float, archivo: str, password: str, password_vendedor: str) -> bool:
    """Función que permite comprar un producto de otro usuario."""

    datos = cargarJSON(archivo)
    # Elimina el producto comprado y suma el dinero al vendedor.
    for registro in datos:
        if registro["usuario"] == vendedor:
            for producto in registro["productos"]:
                if producto["tipo"] == tipo and producto["precio"] == precio:
                    datos.remove(registro)
                    registro["productos"].remove(producto)

                    clave = generarClave(registro["salt"], password_vendedor)
                    
                    dinero_registro = float(descifrarAES128(registro["dinero"], clave, registro["iv"], registro["tag_dinero"]))
                    dinero_registro += precio
                    dinero_cifrado, tag_dinero = cifrarAES128(str(dinero_registro), clave, registro["iv"])
                    
                    registro["dinero"] = dinero_cifrado
                    registro["tag_dinero"] = tag_dinero
                    
                    datos.append(registro)
                    
                    # Resta el dinero al comprador.
                    for registro in datos:
                        if registro["usuario"] == comprador:
                            datos.remove(registro)

                            clave = generarClave(registro["salt"], password)
                            
                            dinero_registro = float(descifrarAES128(registro["dinero"], clave, registro["iv"], registro["tag_dinero"]))
                            dinero_registro -= producto["precio"]
                            dinero_cifrado, tag_dinero = cifrarAES128(str(dinero_registro), clave, registro["iv"])
                            
                            registro["dinero"] = dinero_cifrado
                            registro["tag_dinero"] = tag_dinero
                            
                            datos.append(registro)
                            if guardarDatos(datos, "registros.json"):
                                return True

    return False


def ingresoDinero(usuario: str, dinero: float, archivo: str, password: str):
    """Función que ingresa dinero en la cuenta de un usario."""

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)

            clave = generarClave(registro["salt"], password)
            
            dinero_registro = float(descifrarAES128(registro["dinero"], clave, registro["iv"], registro["tag_dinero"]))
            dinero_registro += dinero
            dinero_cifrado, tag_dinero = cifrarAES128(str(dinero_registro), clave, registro["iv"])
            
            registro["dinero"] = dinero_cifrado
            registro["tag_dinero"] = tag_dinero
            
            datos.append(registro)
            if guardarDatos(datos, "registros.json"):
                return True
    
    return False


def eliminarProducto(usuario: str, producto, archivo) -> bool:
    """Función que elimina un producto de un usuario."""

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
    

def verDinero(usuario: str, archivo: str, password: str) -> float:
    """Función para ver el dinero de un usuario."""

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            clave = generarClave(registro["salt"], password)

            dinero = descifrarAES128(registro["dinero"], clave, registro["iv"], registro["tag_dinero"])

            return float(dinero)


def cambiarUsuario(usuario, nuevo_usuario, archivo) -> bool:
    """
    Función para cambiar el nombre usuario de un usuario.
    (NO USADA EN LA SEGUNDA ENTREGA).
    """

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
    """
    Función para cambiar el nombre de un usuario.
    (NO USADA EN LA SEGUNDA ENTREGA).
    """

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
    """
    Función para cambiar los apellidos de un usuario.
    (NO USADA EN LA SEGUNDA ENTREGA).
    """

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)
            registro["apellidos"] = nuevo_apellido
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False

    
def cambiarEmail(usuario, nuevo_email, archivo, password) -> bool:
    """Función para cambiar el email de un usuario."""

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)

            clave = generarClave(registro["salt"], password)
            
            email_cifrado, tag_email = cifrarAES128(nuevo_email, clave, registro["iv"])
            
            registro["email"] = email_cifrado
            registro["tag_email"] = tag_email
            
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False

    
def cambiarTelefono(usuario, nuevo_telefono, archivo, password) -> bool:
    """Función para cambiar el teléfono de un usuario."""

    datos = cargarJSON(archivo)

    for registro in datos:
        if registro["usuario"] == usuario:
            datos.remove(registro)

            clave = generarClave(registro["salt"], password)
            
            telefono_cifrado, tag_telefono = cifrarAES128(nuevo_telefono, clave, registro["iv"])
            
            registro["telefono"] = telefono_cifrado
            registro["tag_telefono"] = tag_telefono
            
            datos.append(registro)
    
    if guardarDatos(datos, "registros.json"):
        return True
    
    return False


def obtenerClaveRSA(usuario, password):
    """Función que descifra la clave privada de un usuario para firmar."""
    
    datos = cargarJSON("registros.json")

    for registro in datos:
        if registro["usuario"] == usuario:
            clave_RSA_cifrada = registro["clave_RSA"]
            clave_RSA = descifrarAES128(clave_RSA_cifrada, generarClave(registro["salt"], password), registro["iv"], registro["tag_clave_RSA"])
            
            return RSAKeyToObject(stringToBytes(clave_RSA))


def obtenerClavePublicaRSA(usuario):
    """Función que obtiene la clave pública de un usuario para verificar."""
    
    nombre_archivo = './certificados_usuarios/' + usuario + '.crt'

    certificado_usuario = x509.load_pem_x509_certificate(
        open(nombre_archivo, 'rb').read(), default_backend())

    return certificado_usuario.public_key()


def cargarDatosClaveCA() -> dict:
    """
    Se devuelve la información de la clave privada de CA.
    Dado que la función sólo contiene un diccionario, se devuelve
    la posición 0 de la lista de datos del JSON.
    """
    
    with open('ca/ca_key.json', 'r') as archivo:
        datos = json.load(archivo)

        return datos[0]
