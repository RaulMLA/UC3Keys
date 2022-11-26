"""Funciones de mecanismos criptográficosy de seguridad."""

import hashlib
import random
import os
import secrets
import uuid
import datetime


from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import (padding, rsa, utils)
from cryptography.hazmat.primitives.serialization import (Encoding, PrivateFormat, NoEncryption)
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.backends import default_backend


def generadorSALT():
    """Generador de secuencia SALT."""
    salt = secrets.token_hex(8)
    return salt

def generadorIV():
    """Generador de secuencia pseudoaleatoria nonce iv para AES128."""
    return bytesToString(os.urandom(16))


def crearFuncionResumenSHA256(valor: str):
    """Creador de funciones resumen mediante el algoritmo SHA512."""
    resumen = hashlib.sha256(valor.encode('ascii'))
    resumen_hex = resumen.hexdigest()
    return resumen_hex


def aplicarHash(valor):
    """Función que aplica un hash a un valor usando la biblioteca cryptography."""
    
    digest = hashes.Hash(hashes.SHA256(), backend = default_backend())
    digest.update(valor)
    hash = digest.finalize()
    return hash


def generarClave(salt: str, password: str):
    """Generador de clave secreta key para AES128 mediante derivación de clave usando
    el salt y la contraseña del usuario."""

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
    """Función que convierte una cadena de caracteres a bytes."""

    resultado = bytes(string, encoding = 'latin-1')
    return resultado


def bytesToString(bytes):
    """Función que convierte una cadena de bytes a una cadena de caracteres."""

    resultado = str(bytes, encoding = 'latin-1')
    return resultado


def generarClavePrivada():
    """Generador de clave privada RSA."""
    
    private_key = rsa.generate_private_key(
        # El exponente es normalmente 65537 (0x010001).
        public_exponent = 65537,
        # Una clave de 2048 bits en RSA proporcinoa 112 bits de seguridad.
        key_size = 2048,
    )

    return private_key

    
def generarClavePublica(clave_privada):
    """Generador de clave pública RSA."""
    
    return clave_privada.public_key()


def firmarRSA(hash_mensaje, clave_privada):
    """Firma usando RSA (usa clave privada)."""

    firma = clave_privada.sign(
        hash_mensaje,
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        utils.Prehashed(hashes.SHA256())
    )

    firma_string = bytesToString(firma)

    return firma_string


def verificarRSA(firma_string, hash_mensaje, clave_publica):
    """Verificación usando RSA (usa clave públoca)."""
    
    firma = stringToBytes(firma_string)

    clave_publica.verify(
        firma,
        hash_mensaje,
        padding.PSS(
            mgf = padding.MGF1(hashes.SHA256()),
            salt_length = padding.PSS.MAX_LENGTH
        ),
        utils.Prehashed(hashes.SHA256())
    )


def RSAKeyToObject(clave):
    """Función que genera un objeto de clave RSA a partir de una clave RSA."""

    # Obtenemos el objeto a partir de la clave generada.
    objeto_clave = serialization.load_pem_private_key(
        clave, password = None, backend = default_backend())

    return objeto_clave


def interpretar_certificado_CA():
    """
    Interpretación de certificado CA donde se muestra:
    - Nombre del emisor
    - Fecha de emisión
    - Fecha de caducidad
    """

    perm_cert = open('./ca/ca.crt', 'rb').read()
    cert = x509.load_pem_x509_certificate(perm_cert, default_backend())

    print('Autoridad: ', cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)
    print('Fecha emisión: ', cert.not_valid_before)
    print('Fecha expiración: ', cert.not_valid_after)


def generarSolicitudCertificado(usuario, nombre, apellidos):
    """Función que genera una solicitud de certificado a la CA."""

    clave_privada = generarClavePrivada()

    builder = x509.CertificateSigningRequestBuilder()

    nombre_bytes = stringToBytes(nombre)
    apellidos_bytes = stringToBytes(apellidos)
    usuario_bytes = stringToBytes(usuario)

    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.USER_ID, usuario),
        x509.NameAttribute(NameOID.GIVEN_NAME, nombre),
        x509.NameAttribute(NameOID.SURNAME, apellidos),
    ]))
    
    builder = builder.add_extension(
        x509.BasicConstraints(ca = False, path_length = None), critical = True,
    )
    request = builder.sign(
        clave_privada, hashes.SHA256()
    )

    nombre_archivo = './certificados_usuarios/' + usuario + '.req'

    with open(nombre_archivo, 'wb') as f:
        f.write(request.public_bytes(Encoding.PEM))
    
    clave = clave_privada.private_bytes(
                encoding = Encoding.PEM,
                format = PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm = NoEncryption(),
            )

    return bytesToString(clave)
 

def descifrarClaveCA(datos, clave_maestra):
    """Función que descifra la clave privada de la CA mediante la clave maestra."""

    derivacion_clave = generarClave(datos["salt"], clave_maestra)

    clave_privada = descifrarAES128(datos["clave"], derivacion_clave, datos["iv"], datos["tag_clave"])

    return RSAKeyToObject(stringToBytes(clave_privada))
