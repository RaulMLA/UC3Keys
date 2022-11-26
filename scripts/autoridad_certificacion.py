"""Archivo con clase para la gestión de la autoridad certificadora."""

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from scripts.operaciones_json import *
from scripts.mecanismos_criptograficos import *
import datetime
import uuid
import os


class AutoridadCertificacion:
    """Clase para la gestión de la autoridad certificadora."""

    clave_maestra = ""

    def cargarClavePrivadaAutoridad(self):
        """Carga la clave privada de la autoridad certificadora."""

        clave_privada_autoridad = descifrarClaveCA(cargarDatosClaveCA(), self.clave_maestra)

        return clave_privada_autoridad


    # Dentro del CA (Certificate Authority):
    def generarCertificado(self, usuario, nombre, apellidos):
        """Genera un certificado firmado por la autoridad de certificación para el usuario indicado."""

        certificado_autoridad = x509.load_pem_x509_certificate(
            open('./ca/ca.crt', 'rb').read(), default_backend())

        clave_privada_autoridad = self.cargarClavePrivadaAutoridad()
    
        nombre_archivo = './certificados_usuarios/' + usuario + '.req'

        solicitud = x509.load_pem_x509_csr(
            open(nombre_archivo, 'rb').read(), default_backend())

        # Generar certificado.
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(solicitud.subject)
        builder = builder.issuer_name(certificado_autoridad.subject)
        builder = builder.not_valid_before(datetime.datetime.now())
        builder = builder.not_valid_after(datetime.datetime.now() + datetime.timedelta(days = 1460))
        builder = builder.public_key(solicitud.public_key())
        builder = builder.serial_number(int(uuid.uuid4()))
        for ext in solicitud.extensions:
            builder = builder.add_extension(ext.value, ext.critical)
        
        certificado = builder.sign(
            private_key = clave_privada_autoridad,
            algorithm = hashes.SHA256(),
            backend = default_backend()
        )

        ruta = './certificados_usuarios/' + usuario + '.crt'

        with open(ruta, 'wb') as f:
            f.write(certificado.public_bytes(serialization.Encoding.PEM))
        
        # Borramos la solicitud y nos quedamos unicamente con el certificado.
        borrar_solicitud = './certificados_usuarios/' + usuario + '.req'
        os.remove(borrar_solicitud)
