"""Menús principales de la aplicación."""

import os
import time
import sys
from scripts.operaciones_json import *
from scripts.mecanismos_criptograficos import *
from scripts.check_parameters import *
from scripts.usuario import Sesion
from scripts.autoridad_certificacion import AutoridadCertificacion


# Usuario actual de la sesión (inicialmente "", ya que el nombre de usuario tiene que ser >4 caracteres).
usuario = Sesion("")

# Autoridad de certificación.
autoridad_certificacion = AutoridadCertificacion()


def masterPassword() -> str:
    """
    *********************************************************************
    *********************************************************************
    **** ESTO NO SERÍA ASÍ EN LA VIDA REAL. LA CONTRASEÑA NO SE      ****
    **** PUEDE MOSTRAR EN EL CÓDIGO Y DEBERÍA SER TOTALMENTE SECRETA ****
    **** PERO PARA ESTA PRÁCTICA USAMOS ESTE MÉTODO PARA MAYOR       ****
    **** SIMPLICIDAD.                                                ****
    ****                                                             ****                   
    **** CONTRASEÑA MAESTRA:                                         ****   
    **** 1234                                                        ****  
    *********************************************************************
    *********************************************************************
    """

    while True:
        os.system("clear")
        print("***** CONTRASEÑA MAESTRA *****")
        password = getpass.getpass("Contraseña: ")

        return password


def start():
    """Menú que se ejecuta una sóla vez al ejecutar el programa y pide
    la contraseña maestra hasta que sea correcta."""

    intentos = 0

    while True:
        try:
            autoridad_certificacion.clave_maestra = masterPassword()
            autoridad_certificacion.cargarClavePrivadaAutoridad()
            break
        except:
            intentos += 1
            print("\n[ERROR]\nContraseña maestra incorrecta.")

            if intentos > 3:
                print("\nVuelva a intentarlo en 3 segundos.")
                time.sleep(3)

            os.system ("clear")
    
    menuInicio()


def menuInicio():
    """MENÚ INICIO: Opciones de iniciar sesión o registrase."""

    right_choice = False

    while not right_choice:
        os.system("clear")
        print("¡Bienvenido a UC3Keys!")
        print("\nOperaciones disponibles:")
        print("[1] Iniciar sesión.")
        print("[2] Registrarse.")
        print("\n[0] Salir")

        choice = input("\nSelecciona la operación que desea llevar a cabo: ")

        if choice == "0":
            right_choice = True
            print("\nSaliendo de UC3Keys...")
            time.sleep(2)
            os.system("clear")
            sys.exit(0)
        elif choice == "1":
            right_choice = True
            usuario.usuario, usuario.password = menuInicioSesion()
            menuPrincipal()
        elif choice == "2":
            right_choice = True
            menuRegistro()
        else:
            print(
                "\n[Error] Operación incorrecta.\nVuelva a intentarlo en 3 segundos."
            )
            time.sleep(3)
            os.system("clear")

    return True


def menuInicioSesion():
    """MENÚ INICIO SESIÓN: Para que el usuario pueda iniciar sesión."""
    
    os.system("clear")

    condition = False
    intentos = 0

    while not condition:
        os.system("clear")
        print("-- INICIO DE SESIÓN --\n")
        usuario = input("Usuario: ")
        password = getpass.getpass("Contraseña: ")

        if buscarUsuario(usuario, "registros.json"):
            datos_usuario = buscarUsuario(usuario, "registros.json")
            hash = crearFuncionResumenSHA256(datos_usuario['salt'] + password)
            if hash == datos_usuario["password"]:
                # Aquí podríamos cambiar el salt para que no sea igual siempre.
                condition = True
            else:
                print("\n[ERROR]\nContraseña incorrecta.\n")
                time.sleep(1)
                intentos += 1
                if intentos > 3:
                    print("Vuelva a intentarlo en 5 segundos.")
                    time.sleep(5)
        else:
            print("\n[ERROR]\nUsuario no encontrado.\n")
            time.sleep(1)
            intentos += 1
            if intentos > 3:
                print("Vuelva a intentarlo en 5 segundos.")
                time.sleep(5)

    # Devolvemos el nombre del usuario que ha iniciado sesión correctamente.
    return usuario, password


def menuRegistro():
    """MENÚ REGISTRO: Para que el usuario pueda registrarse."""
    
    os.system("clear")

    print("-- FORMULARIO DE REGISTRO --\n")

    usuario = checkUsuario()
    nombre = checkNombre()
    apellidos = checkApellidos()
    email = checkEmail()
    telefono = checkTelefono()
    password = checkPassword()
    
    # Generamos un certificado para el usuario.
    clave_RSA = generarSolicitudCertificado(usuario, nombre, apellidos)
    autoridad_certificacion.generarCertificado(usuario, nombre, apellidos) 

    guardarRegistro(usuario, nombre, apellidos, email, telefono, password, clave_RSA)

    print("\nUsuario {0} registrado correctamente.\nRedirigiendo...".format(
        usuario))
    time.sleep(2)
    os.system("clear")

    menuInicio()


def menuPrincipal():
    """MENÚ PRINCIPAL: Menú principal de la aplicación donde se encuentran las principales operaciones posibles."""

    intentos = 0

    while True:
        os.system("clear")
        print("\nUC3Keys")
        print("\nOperaciones disponibles:")
        print("[1] Ver y comprar productos.")
        print("[2] Subir producto.")
        print("[3] Ver mis productos.")
        print("[4] Ver y modificar información de perfil.")
        print("[5] Ingresar dinero.")
        print("\n[0] Cerrar sesión.")

        choice = input("\nSelecciona la operación que desea llevar a cabo: ")

        if choice == "0":
            usuario.usuario = ""
            print("\nCerrando sesión...")
            time.sleep(1)
            os.system("clear")
            menuInicio()
        elif choice == "1":
            usuario.verProductos()
        elif choice == "2":
            usuario.subirProducto()
        elif choice == "3":
            usuario.misProductos()
        elif choice == "4":
            usuario.informacionPerfil()
        elif choice == "5":
            usuario.ingresarDinero()
        else:
            print("\n[Error] Operación incorrecta.\n")
            time.sleep(1)
            intentos += 1
            if intentos > 3:
                print("Vuelva a intentarlo en 5 segundos.")
                time.sleep(5)
