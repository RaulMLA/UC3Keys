"""Funciones de mecanismos criptográficosy de seguridad."""

import hashlib
import random
import os
import secrets


from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
#from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generadorSALT():
    """Generador de secuencia SALT."""
    salt = secrets.token_hex(8)
    return salt

def generadorIV():
    """Generador de secuencia pseudoaleatoria nonce iv para AES128."""
    return bytesToString(os.urandom(16))


def crearFuncionResumenSHA256(valor: str):
    """Creador de funciones resumen mediante el algoritmo SHA512"""
    resumen = hashlib.sha256(valor.encode('ascii'))
    resumen_hex = resumen.hexdigest()
    return resumen_hex


def generarClave(salt: str, password: str):
    """Generador de clave secreta key para AES128 mediante derivación de clave usando
    el salt y la función resumen del salt + contraseña del usuario."""

    salt_bytes = stringToBytes(salt)
    password_bytes = stringToBytes(password)
    
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 16,
        salt = salt_bytes,
        iterations = 390000,
    )
    
    key_bytes = kdf.derive(password_bytes)

    return key_bytes
    

def cifrarAES128(valor: str, key, iv_string):
    """Cifrado AES (Advanced Encryption Standard) con longitud de clave de128 bits."""

    iv = stringToBytes(iv_string)
    
    valor_bytes = stringToBytes(valor)

    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    texto_cifrado = encryptor.update(valor_bytes) + encryptor.finalize()

    return bytesToString(texto_cifrado), bytesToString(encryptor.tag)


def descifrarAES128(valor: str, key, iv_string, tag_string):
    """Descifrado AES (Advanced Encryption Standard) con longitud de clave de128 bits."""

    iv = stringToBytes(iv_string)
    tag = stringToBytes(tag_string)
    
    decipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = decipher.decryptor()

    valor_cifrado = stringToBytes(valor)
    
    result = decryptor.update(valor_cifrado) + decryptor.finalize()

    return bytesToString(result)


def stringToBytes(string):
    resultado = bytes(string, encoding = 'latin-1')
    return resultado


def bytesToString(bytes):
    resultado = str(bytes, encoding = 'latin-1')
    return resultado
