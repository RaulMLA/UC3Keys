"""Funciones de mecanismos criptográficosy de seguridad."""

import hashlib
import random
import os
import secrets


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash


def generadorSALT():
    """Generador de secuencia SALT."""
    salt = secrets.token_hex(8)
    return salt


def crearFuncionResumenSHA256(valor: str):
    """Creador de funciones resumen mediante el algoritmo SHA512"""
    resumen = hashlib.sha256(valor.encode('ascii'))
    resumen_hex = resumen.hexdigest()
    return resumen_hex


def generarClave():
    """Esta función genera una clave de Fernet. Es muy importante mantener la
    clave en un sitio seguro. En caso de perder la clave, no será posible
    descifrar mensajes que han sido cifrados con ella. Si alguien consigue el
    acceso a esta clave, podrán descifrar los mensajes y de tomar el control."""
    key = Fernet.generate_key()
    key_str = key.decode()
    return key_str

    
def cifrarAES128(valor: str, key: str):
    key_bytes = bytes(key, 'utf-8')
    key_obj = Fernet(key_bytes)
    token = key_obj.encrypt(bytes(valor, 'utf-8'))
    return token.decode()
    

def descifrarAES128(valor: str, key):
    key_bytes = bytes(key, 'utf-8')
    key_obj = Fernet(key_bytes)
    token = key_obj.decrypt(bytes(valor, 'utf-8'))
    return token.decode()
