# Generación de CA (Autoridad de Certificación) y su certificado autofirmado.
# (Ejecutar estos comandos en el directorio raíz del proyecto para generar la CA).

# Se crea un request (ca.req) y una clave privada RSA con tamaño de clave 2048 bits (ca.key).
openssl req -new -newkey rsa:2048 -keyout ./ca.key -out ./ca.req -nodes

# Country Name (2 letter code) []: ES
# State or Province Name (full name) []: Madrid
# Locality Name (eg, city) []: Leganes
# Organization Name (eg, company) []: UC3Keys
# Organizational Unit Name (eg, section) []: UC3Keys
# Common Name (eg, fully qualified host name) []: UC3Keys
# Email Address []: uc3keys@uc3m.es
# A challenge password []: 71ji24b7v23823bvs82n

# CA autofirma su certificado (válido por 25 años) y lo guarda (ca.crt).
openssl x509 -req -days 9125 -in ./ca.req -signkey ./ca.key -out ./ca.crt

# Ver certificado de la CA.
# openssl x509 -in ./ca.crt -text -noout
