"""Funciones de comprobación de campos."""
import re
import os
import time
import getpass
from operaciones_json import *


# Archivo para comprobar cada uno de los parámetros usados.
def checkPassword() -> str:
    """
    Función que comprueba si la contraseña es correcta.
    Una contraseña es correcta si:
    · Tiene entre 8 y 20 caracteres.
    · Contiene al menos un número.
    · Contiene al menos una mayúscula.
    · Contiene al menos una minúscula.
    · Contiene al menos un caracter especial.
    """
    regex = re.compile('^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

    while True:
        password = getpass.getpass("Contraseña: ")
        confirmar_password = getpass.getpass("Confirmar contraseña: ")

        if re.search(regex, password):
            if password == confirmar_password:
                return password
            else:
                print("\n[ERROR]\nLas contraseñas no coinciden.\nVuelva a intentarlo en 5 segundos.\n")
                time.sleep(5)
        else:
            print("\n[ERROR]\nLa contraseña debe tener entre 8 y 20 caracteres.")
            print("La contraseña debe tener al menos un número.")
            print("La contraseña debe tener al menos una letra mayúscula.")
            print("La contraseña debe tener al menos una letra minúscula.")
            print("La contraseña debe tener al menos un caracter especial.")
            print("\nVuelva a intentarlo en 5 segundos.\n")
            time.sleep(5)


def checkEmail() -> str:
    """
    Función que comprueba si el nombre de un usuario es correcto.
    Un nombre es correcto si:
    · Tiene entre 1 y 20 caracteres.
    · No contiene números ni caracteres especiales.
    · Puede contener espacios.
    """

    regex = re.compile('^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$')
    
    while True:
        email = input("Email: ")
        if (re.search(regex, email)):
            return email
        print("\n[ERROR]\nEl email debe tener la forma aaaa@bbbb.cccc")
        print("\nVuelva a intentarlo en 5 segundos.\n")
        time.sleep(5)


def checkNombre() -> str:
    """
    Función que comprueba si el nombre de un usuario es correcto.
    Un nombre es correcto si:
    · Tiene entre 1 y 20 caracteres.
    · No contiene números ni caracteres especiales.
    · Puede contener espacios.
    """

    regex = re.compile('^[A-Za-z\s]{1,20}$')
    
    while True:
        nombre = input("Nombre: ")
        if (re.search(regex, nombre)):
            return nombre

        print("\n[ERROR]\nEl nombre debe tener menos de 20 caracteres.")
        print("El nombre no puede contener números ni caracteres especiales.")
        print("El nombre no puede contener tildes.")
        print("\nVuelva a intentarlo en 5 segundos.\n")
        time.sleep(5)


def checkApellidos() -> str:
    """
    Función que comprueba si los apellidos de un usuario son correctos.
    Un apellido es correcto si:
    · Tiene menos entre 1 y 40 caracteres.
    · No contiene números ni caracteres especiales.
    · Puede contener espacios.
    """

    regex = re.compile('^[A-Za-z\s]{1,40}$')
    
    while True:
        apellidos = input("Apellidos: ")
        if (re.search(regex, apellidos)):
            return apellidos
        print("\n[ERROR]\nLos apellidos deben tener menos de 40 caracteres.")
        print("Los apellidos no puede contener números ni caracteres especiales.")
        print("El apellido no puede contener tildes.")
        print("\nVuelva a intentarlo en 5 segundos.\n")
        time.sleep(5)

        
def checkLicencia() -> str:
    """
    Función que comprueba si una licencia de producto es correcta.
    Un nombre de usuario es correcto si:
    · Tiene entre 5 y 20 caracteres.
    · Puede contener letras y números.
    """

    regex = re.compile('^[A-Za-z0-9]{5,20}$')
    
    while True:
        licencia = input("\nNúmero de licencia: ")
        confirmar_licencia = input("\nConfirmar número de licencia: ")
        
        if (re.search(regex, licencia)):
            if licencia == confirmar_licencia:
                return licencia
            else:
                print("\n[ERROR]\nLas licencias no coinciden.\nVuelva a intentarlo en 5 segundos.\n")
                time.sleep(5)
        else:
            print("\n[ERROR]\nLa licencia debe tener entre 5 y 20 caracteres.")
            print("La licencia puede contener letras y números.")
            print("\nVuelva a intentarlo en 5 segundos.\n")
            time.sleep(5)
        

def checkTelefono() -> str:
    """
    Función que comprueba si un número de teléfono es correcto.
    Un número de teléfono es correcto si:
    · Tiene 9 dígitos.
    """

    regex = re.compile('^[0-9]{9}$')
    
    while True:
        telefono = input("Número de teléfono: ")
        if (re.search(regex, telefono)):
            return telefono
        print("\n[ERROR]\nEl número de teléfono tiene que tener 9 dígitos.")
        print("\nVuelva a intentarlo en 5 segundos.\n")
        time.sleep(5)
        

def checkPrecio() -> bool:
     while True:
        precio = input("\nPrecio del artículo: ")

        try:
            return float(precio)
        except:
            print("\n[ERROR]\nEl precio tiene que ser un número.")
            print("\nVuelva a intentarlo en 5 segundos.\n")
            time.sleep(5)


def checkDinero() -> bool:
     while True:
        dinero = input("\nCantidad de dinero a ingresar: ")

        try:
            return float(dinero)
        except:
            print("\n[ERROR]\nEl dinero tiene que ser un número.")
            print("\nVuelva a intentarlo en 5 segundos.\n")
            time.sleep(5)
            

def checkUsuario() -> str:
    """
    Función que comprueba si el nombre de usuario es correcto.
    Un nombre de usuario es correcto si:
    · Tiene entre 5 y 12 caracteres.
    · El primer caracter es una letra.
    · Puede contener guiones bajos, letras y números.
    """

    regex = re.compile('^[A-Za-z][A-Za-z0-9_]{4,11}$')
    
    while True:
        usuario = input("Usuario: ")
        if not buscarUsuario(usuario, "registros.json"):
            if (re.search(regex, usuario)):
                return usuario
            else:
                print("\n[ERROR]\nEl nombre de usuario debe tener entre 5 y 12 caracteres.")
                print("El nombre de usuario tiene que empezar por una letra.")
                print("El nombre de usuario puede contener guiones bajos, letras y números.")
                print("\nVuelva a intentarlo en 5 segundos.\n")
                time.sleep(5)
        else:
            print("\n[ERROR]\nEl usuario ya está registrado.\nVuelva a intentarlo en 5 segundos.\n")
            time.sleep(5)
            
