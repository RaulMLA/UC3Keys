import os
import time
import sys
from operaciones_json import *
from mecanismos_criptograficos import *
from check_parameters import *
from usuario import Sesion


# Usuario actual de la sesión (inicialmente "", ya que el nombre de usuario tiene que ser >4 caracteres).
usuario = Sesion("")


# MENÚ INICIO: Opciones de iniciar sesión o registrase.
def menuInicio():
    right_choice = False

    while not right_choice:
        os.system ("clear")
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
            os.system ("clear")
            sys.exit(0)
        elif choice == "1":
            right_choice = True
            usuario.usuario = menuInicioSesion()
            menuPrincipal()
        elif choice == "2":
            right_choice = True
            menuRegistro()
        else:
            print("\n[Error] Operación incorrecta.\nVuelva a intentarlo en 5 segundos.")
            time.sleep(5)
            os.system ("clear")

    return True


def menuInicioSesion():
    os.system ("clear")

    condition = False

    while not condition:
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
                print("\n[ERROR] Contraseña incorrecta.\nVuelva a intentarlo en 5 segundos.")
                time.sleep(5)
                os.system ("clear")
        else:
            print("\n[ERROR] Usuario no encontrado.\nVuelva a intentarlo en 5 segundos.")
            time.sleep(5)
            os.system ("clear")

    # usuario tiene que estar en el json
    # aplicar funcion resumen a contraseña
    # comparar resumen con el que hay en el json asociado al usuario

    # Aviso de prueba.
    print("\nUsuario {0} ha iniciado sesión con contraseña {1}." .format(usuario, password))

    # Devolvemos el nombre del usuario que ha iniciado sesión correctamente.
    return usuario


def menuRegistro():
    os.system ("clear")

    print("-- FORMULARIO DE REGISTRO --\n")
    
    usuario = checkUsuario()
    nombre = checkNombre()
    apellidos = checkApellidos()
    email = checkEmail()
    telefono = checkTelefono()
    password = checkPassword()

    guardarRegistro(usuario, nombre, apellidos, email, telefono, password)

    print("\nUsuario {0} registrado correctamente.\nRedirigiendo..." .format(usuario))
    time.sleep(3)
    os.system ("clear")

    menuInicio()


def menuPrincipal():
    os.system ("clear")
    print("\nUC3Keys")
    
    while True:
        print("\nOperaciones disponibles:")
        print("[1] Ver productos.")
        print("[2] Subir producto.")
        print("[3] Ver mis productos.")
        print("[4] Información de perfil.")
        print("[5] Ingresar dinero.")
        print("\n[0] Cerrar sesión.")

        choice = input("\nSelecciona la operación que desea llevar a cabo: ")

        if choice == "0":
            # Borramos el usuario de la sesión (no hay nadie conectado).
            usuario.usuario = ""
            print("\nCerrando sesión...")
            time.sleep(2)
            os.system ("clear")
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
            print("\n[Error] Operación incorrecta.\nVuelva a intentarlo en 5 segundos.")
            time.sleep(5)
            os.system ("clear")

        menuPrincipal()
    


# Ejecutamos la aplicación.
if __name__ == "__main__":
    menuInicio()
