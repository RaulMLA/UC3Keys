from math import prod
from mecanismos_criptograficos import *
from operaciones_json import *
from check_parameters import *
import os
import time



class Sesion:
    """Clase que representa una sesión de un usuario"""
    def __init__(self, usuario: str):
        self.usuario = usuario


    def verProductos(self):
        """Método que muestra todos los productos que no son del propio usuario."""

        productos = obtenerProductos(self.usuario, "registros.json")

        counter = 1

        os.system ("clear")
        print("+------------------- PRODUCTOS DISPONIBLES -------------------+\n")
        print("+-----+---------------+--------------------------+------------+")
        print("|ID   |VENDEDOR       |TIPO                      |PRECIO (€)  |")
        print("+-----+---------------+--------------------------+------------+")
        print("+-----+---------------+--------------------------+------------+")

        for producto in productos:
            print("|{:<5}|{:<15}|{:<26}|{:<12}|".format(counter, producto['usuario'], producto['tipo'], producto['precio']))
            print("+-----+---------------+--------------------------+------------+")
            counter += 1
        print("\n[0] Volver al menú.")
        
        item = int(input("\nSelecciona el producto que quieres comprar: "))

        if item == 0:
            print("\nVolviendo al menú...")
            time.sleep(2)
            os.system ("clear")
            return

        if item in range (1, len(productos) + 1):
            producto_seleccionado = productos[item - 1]
            if verDinero(self.usuario, "registros.json") >= producto_seleccionado["precio"]:
                if comprarProducto(self.usuario, producto_seleccionado["usuario"], producto_seleccionado["tipo"], producto_seleccionado["precio"], "registros.json"):
                    print("\nProducto {0} comprado por {1}€ correctamente.\nSu clave de licencia es: {2}" .format(producto_seleccionado["tipo"], producto_seleccionado["precio"], descifrarAES128(producto_seleccionado["licencia"], (buscarUsuario(producto_seleccionado["usuario"], "registros.json"))["clave"])))
                    while True:
                        exit = input("\nGuarde su licencia y escriba '0' para salir: ")
                        if exit == "0":
                            break
                        print("\n[ERROR]\nNo ha pulsado la tecla correcta.\nVuelva a intentarlo en 5 segundos.")
                        time.sleep(5)
                else:
                    print("\n[ERROR] Error durante la compra.\nVuelva a intentarlo en 5 segundos.")
            else:
                print("\n[ERROR] No tienes dinero suficiente.\nVuelva a intentarlo en 5 segundos.")
        else:
            print("\n[ERROR] Producto incrrecto.\nVuelva a intentarlo en 5 segundos.")

        time.sleep(5)
        os.system ("clear")
        self.verProductos()

        
    def subirProducto(self):
        """Método que permite al usuario crear un nuevo producto."""

        os.system ("clear")

        while True:
            print("\nTipos disponibles:")
            print("[1] Windows 10")
            print("[2] Windows 11")
            print("[3] Microsoft 365")
            print("[4] Adobe Creative Cloud")
            print("[5] Norton 360")
            print("[6] McAfee")
            print("[7] Kaspersky 2022")
            print("\n[0] Volver al menú.")

            seleccion = input("\nSelecciona el tipo de artículo: ")

            if seleccion == "0":
                print("\nVolviendo al menú...")
                time.sleep(2)
                os.system ("clear")
                return
            elif seleccion == "1":
                tipo = "Windows 10"
            elif seleccion == "2":
                tipo = "Windows 11"
            elif seleccion == "3":
                tipo = "Microsoft 365"
            elif seleccion == "4":
                tipo = "Adobe Creative Cloud"
            elif seleccion == "5":
                tipo = "Norton 360"
            elif seleccion == "6":
                tipo = "McAfee"
            elif seleccion == "7":
                tipo = "Kaspersky 2022"
            else:
                tipo = 0
            
            if tipo != 0:
                precio = checkPrecio()
                licencia = checkLicencia()

                if guardarLicencia(self.usuario, tipo, precio, licencia, "registros.json"):
                    print("\nLicencia de {0} subida por {1}€ satisfactoriamente.\nVolviendo al menú..." .format(tipo, precio))
                    time.sleep(5)
                    os.system ("clear")
                    return
                else:
                    print("\n[ERROR] No se ha podido subir el producto.\nVuelva a intentarlo en 5 segundos.")
                    time.sleep(5)

            else:
                print("\n[ERROR] Tipo de licencia incorrecta.\nVuelva a intentarlo en 5 segundos.")
                time.sleep(5)
                os.system ("clear")


    def verMisProductos(self):
        """Método que muestra mis productos."""
        productos = obtenerMisProductos(self.usuario, "registros.json")

        counter = 1

        os.system ("clear")
        print("+--------------- MIS PRODUCTOS ---------------+\n")
        print("+-----+--------------------------+------------+")
        print("|ID   |TIPO                      |PRECIO (€)  |")
        print("+-----+--------------------------+------------+")
        print("+-----+--------------------------+------------+")

        for producto in productos:
            print("|{:<5}|{:<26}|{:<12}|".format(counter, producto['tipo'], producto['precio']))
            print("+-----+--------------------------+------------+")
            counter += 1

        return productos

    
    def misProductos(self):
        """Método que permite modificar mis productos."""
        
        productos = self.verMisProductos()

        condition = False

        print("\n[0] Volver al menú.")

        while True:
                try:
                    id = int(input("Selecciona el artículo que quieres eliminar: "))
                    if id in range (0, len(productos) + 1):
                        break
                except:
                    print("\n[ERROR]\nArtículo incorrecto.\nVuelva a intentarlo en 5 segundos.")
                    time.sleep(5)
                    os.system ("clear")

        if id == 0:
            print("\nVolviendo al menú...")
            time.sleep(2)
            os.system ("clear")
            return

        eliminarProducto(self.usuario, productos[id - 1], "registros.json")

        print("\nProducto {0} eliminado correctamente." .format(productos[id - 1]["tipo"]))
        print("\nVolviendo al menú...")
        time.sleep(2)
        os.system ("clear")


    def informacionPerfil(self):
        """Método que muestra la información del perfil y permite hacer cambios."""
        informacion = buscarUsuario(self.usuario, "registros.json")

        # Desciframos los datos cifrados.
        email = descifrarAES128(informacion["email"], informacion["clave"])
        telefono = descifrarAES128(informacion["telefono"], informacion["clave"])
        dinero = descifrarAES128(informacion["dinero"], informacion["clave"])

        os.system ("clear")
        print("\nTu información:\nNombre de usuario: {0}\nNombre: {1}\nApellidos: {2}\nEmail: {3}\nNúmero de teléfono: {4}\nDinero disponible: {5}" .format(informacion["usuario"], informacion["nombre"], informacion["apellidos"], email, telefono, dinero))
        
        
        print("\nModificaciones disponibles:")
        print("[1] Usuario")
        print("[2] Nombre")
        print("[3] Apellidos")
        print("[4] Email")
        print("[5] Teléfono")
        print("[6] Contraseña")
        print("\n[0] Volver al menú.")

        seleccion = input("\nSelecciona el dato que quieres modificar: ")

        if seleccion == "0":
            print("\nVolviendo al menú...")
            time.sleep(2)
            os.system ("clear")
            return
        elif seleccion == "1":
            nuevo_usuario = checkUsuario()
            cambiarUsuario(self.usuario, nuevo_usuario, "registros.json")
            self.usuario = nuevo_usuario
            print("\nNombre cambiado a {0} correctamente." .format(nuevo_usuario))
            time.sleep(2)
        elif seleccion == "2":
            nuevo_nombre = checkNombre()
            cambiarNombre(self.usuario, nuevo_nombre, "registros.json")
            print("\nNombre cambiado a {0} correctamente." .format(nuevo_nombre))
            time.sleep(2)
        elif seleccion == "3":
            nuevo_apellido = checkApellidos()
            cambiarApellidos(self.usuario, nuevo_apellido, "registros.json")
            print("\nApellidos cambiados a {0} correctamente." .format(nuevo_apellido))
            time.sleep(2)
        elif seleccion == "4":
            nuevo_email = checkEmail()
            cambiarEmail(self.usuario, nuevo_email, "registros.json")
            print("\nEmail cambiado a {0} correctamente." .format(nuevo_email))
            time.sleep(2)
        elif seleccion == "5":
            nuevo_telefono = checkTelefono()
            cambiarTelefono(self.usuario, nuevo_telefono, "registros.json")
            print("\nTeléfono cambiado a {0} correctamente." .format(nuevo_telefono))
            time.sleep(2)
        elif seleccion == "6":
            nueva_pass = checkPassword()
            cambiarPass(self.usuario, nueva_pass, "registros.json")
            print("\nContraseña cambiada correctamente.")
            time.sleep(2)
        else:
            print("\n[ERROR] Tipo de acción incorrecta.\nVuelva a intentarlo en 5 segundos.")
            time.sleep(5)
            os.system ("clear")

        self.informacionPerfil()

            
    def ingresarDinero(self):
        """Método que permite ingresar dinero en la cuenta del usuario."""
        dinero = checkDinero()

        if ingresoDinero(self.usuario, dinero, "registros.json"):
            print("\nSe han ingresado correctamente {0}€ a la cuenta del usuario {1}." .format(dinero, self.usuario))
            time.sleep(5)
            os.system ("clear")
        else:
            print("\n[ERROR]\nNo se ha podido ingresar el dinero.\nVuelva a intentarlo en 5 segundos.\nVolviendo al menú...")
            time.sleep(5)
            os.system ("clear")

