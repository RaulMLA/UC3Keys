"""Archivo que contiene la clase Sesion, la cual representa la sesión actual de un
usuario registrado. Cuenta con funciones que el usuario puede realizar desde el menú."""

from math import prod
from scripts.mecanismos_criptograficos import *
from scripts.operaciones_json import *
from scripts.check_parameters import *
from scripts.menus import *
import os
import time



class Sesion:
    """Clase que representa una sesión de un usuario"""
    def __init__(self, usuario: str):
        # Nombre del usuario almacenado en memoria durante la sesión del usuario.
        self.usuario = usuario
        # Contraseña del usuario almacenada en memoria durante la sesión del usuario.
        # Este dato es imprescindible para el cifrado/descifrado en la sesión.
        self.password = ""


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

        while True:
            try:
                item = int(input("\nSelecciona el producto que quieres comprar: "))
                break
            except:
                print("\n[ERROR]\nDebes introducir un número.\nVuelva a intentarlo en 3 segundos.")
                time.sleep(3)
                os.system ("clear")
                self.verProductos()
            
        if item == 0:
            print("\nVolviendo al menú...")
            time.sleep(1)
            os.system ("clear")
            return

        if item in range (1, len(productos) + 1):
            producto_seleccionado = productos[item - 1]
            if verDinero(self.usuario, "registros.json", self.password) >= producto_seleccionado["precio"]:
                
                # SIMULACIÓN DE CONFIRMACIÓN DE LA COMPRA POR PARTE DE VENDEDOR.
                # El comprador tiene que iniciar sesión para confirmar la compra.
                print("\n[INFO]\nEl vendedor {0} tiene que iniciar sesión para confirmar la compra:" .format(producto_seleccionado["usuario"]))
                
                condition = False
                intentos = 0

                while not condition:
                    print("\n-- INICIO DE SESIÓN (VENDEDOR {0}) --\n" .format(producto_seleccionado["usuario"]))
                    vendedor = input("Usuario: ")
                    password_vendedor = getpass.getpass("Contraseña: ")

                    if buscarUsuario(vendedor, "registros.json"):
                        datos_usuario = buscarUsuario(vendedor, "registros.json")
                        hash = crearFuncionResumenSHA256(datos_usuario['salt'] + password_vendedor)
                        if hash == datos_usuario["password"]:
                            # Aquí podríamos cambiar el salt para que no sea igual siempre, pero lo mantenemos así por simplicidad.
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

                if vendedor == producto_seleccionado["usuario"]:

                    # Verificación del producto para comprobar su integridad antes de ser comprado.
                    string_producto = stringProducto(producto_seleccionado["usuario"], producto_seleccionado["tipo"], producto_seleccionado["precio"], producto_seleccionado["licencia"], producto_seleccionado["tag_licencia"])
                    hash_producto = aplicarHash(stringToBytes(string_producto))
                    clave_publica = obtenerClavePublicaRSA(vendedor)
                    firma_string = producto_seleccionado["firma_producto"]

                    try:
                        verificarRSA(firma_string, hash_producto, clave_publica)
                    except:
                        print("\nEl producto no mantiene su integridad o no ha podido ser verificado.\nVolviendo al menú de productos...")
                        time.sleep(3)
                        os.system ("clear")
                        self.verProductos()
                    
                    print("\nProducto verificado correctamente.")
                    time.sleep(3)
                    os.system ("clear")

                    # Si se ha verificado el producto, se compra.
                    if comprarProducto(self.usuario, vendedor, producto_seleccionado["tipo"], producto_seleccionado["precio"], "registros.json", self.password, password_vendedor):
                        usuario = buscarUsuario(producto_seleccionado["usuario"], "registros.json")
                        clave = generarClave(usuario["salt"], password_vendedor)
                        licencia = descifrarAES128(producto_seleccionado["licencia"], clave, usuario["iv"], producto_seleccionado["tag_licencia"])
                        print("\nProducto {0} comprado por {1}€ correctamente.\nSu clave de licencia es: {2}" .format(producto_seleccionado["tipo"], producto_seleccionado["precio"], licencia))
                        while True:
                            exit = input("\nGuarde su licencia y escriba '0' para salir: ")
                            if exit == "0":
                                break
                            print("\n[ERROR]\nNo ha pulsado la tecla correcta.\nVuelva a intentarlo.")
                            time.sleep(1)
                    else:
                        print("\n[ERROR]\nError durante la compra.\nVuelva a intentarlo en 3 segundos.")
                else:
                    print("\n[ERROR]\nEl usuario no coincide con el vendedor.\nVuelva a intentarlo en 3 segundos.")
            else:
                print("\n[ERROR]\nNo tienes dinero suficiente.\nVuelva a intentarlo en 3 segundos.")
        else:
            print("\n[ERROR]\nProducto incrrecto.\nVuelva a intentarlo en 3 segundos.")

        time.sleep(3)
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
                time.sleep(1)
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

                if guardarLicencia(self.usuario, tipo, precio, licencia, "registros.json", self.password):
                    print("\nLicencia de {0} firmada y subida por {1}€ satisfactoriamente.\nVolviendo al menú..." .format(tipo, precio))
                    time.sleep(3)
                    os.system ("clear")
                    return
                else:
                    print("\n[ERROR]\nNo se ha podido subir el producto.\nVuelva a intentarlo en 3 segundos.")
                    time.sleep(3)

            else:
                print("\n[ERROR]\nTipo de licencia incorrecta.\nVuelva a intentarlo en 3 segundos.")
                time.sleep(3)
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

            while True:
                try:
                    id = int(input("\nSelecciona el artículo que quieres eliminar: "))
                    break
                except:
                    print("\n[ERROR]\nDebes introducir un número.\nVuelva a intentarlo en 3 segundos.")
                    time.sleep(3)
            
            if id in range (0, len(productos) + 1):
                break
            else:
                print("\n[ERROR]\nArtículo incorrecto.\nVuelva a intentarlo en 3 segundos.")
                time.sleep(3)

        if id == 0:
            print("\nVolviendo al menú...")
            time.sleep(1)
            os.system ("clear")
            return

        eliminarProducto(self.usuario, productos[id - 1], "registros.json")

        print("\nProducto {0} eliminado correctamente." .format(productos[id - 1]["tipo"]))
        print("\nVolviendo al menú...")
        time.sleep(1)
        os.system ("clear")


    def informacionPerfil(self):
        """Método que muestra la información del perfil y permite hacer cambios."""
        informacion = buscarUsuario(self.usuario, "registros.json")

        # Desciframos los datos cifrados.

        clave = generarClave(informacion["salt"], self.password)
        
        email = descifrarAES128(informacion["email"], clave, informacion["iv"], informacion["tag_email"])
        telefono = descifrarAES128(informacion["telefono"], clave, informacion["iv"], informacion["tag_telefono"])
        dinero = descifrarAES128(informacion["dinero"], clave, informacion["iv"], informacion["tag_dinero"])

        os.system ("clear")
        print("\nTu información:\nNombre de usuario: {0}\nNombre: {1}\nApellidos: {2}\nEmail: {3}\nNúmero de teléfono: {4}\nDinero disponible: {5}€" .format(informacion["usuario"], informacion["nombre"], informacion["apellidos"], email, telefono, dinero))
        
        
        print("\nModificaciones disponibles:")
        print("[1] Email")
        print("[2] Teléfono")
        print("\n[0] Volver al menú.")

        seleccion = input("\nSelecciona el dato que quieres modificar: ")

        if seleccion == "0":
            print("\nVolviendo al menú...")
            time.sleep(1)
            os.system ("clear")
            return
        elif seleccion == "1":
            nuevo_email = checkEmail()
            cambiarEmail(self.usuario, nuevo_email, "registros.json", self.password)
            print("\nEmail cambiado a {0} correctamente." .format(nuevo_email))
            time.sleep(2)
        elif seleccion == "2":
            nuevo_telefono = checkTelefono()
            cambiarTelefono(self.usuario, nuevo_telefono, "registros.json", self.password)
            print("\nTeléfono cambiado a {0} correctamente." .format(nuevo_telefono))
            time.sleep(2)
        else:
            print("\n[ERROR]\nTipo de acción incorrecta.\nVuelva a intentarlo en 3 segundos.")
            time.sleep(3)
            os.system ("clear")

        self.informacionPerfil()

            
    def ingresarDinero(self):
        """Método que permite ingresar dinero en la cuenta del usuario."""
        os.system ("clear")
        print("-- INGRESO DE DINERO --")
        dinero = checkDinero()

        if ingresoDinero(self.usuario, dinero, "registros.json", self.password):
            print("\nSe han ingresado correctamente {0}€ a la cuenta del usuario {1}." .format(dinero, self.usuario))
            time.sleep(2)
            os.system ("clear")
        else:
            print("\n[ERROR]\nNo se ha podido ingresar el dinero.\nVuelva a intentarlo en 3 segundos.\nVolviendo al menú...")
            time.sleep(3)
            os.system ("clear")

