Grupo 8208

Raúl Manzanero López-Aguado (100451106)
Adrián Sánchez del Cerro (100451195)

------------

EJECUCIÓN:

- Ejecutar archivo main.py para comenzar la ejecución del programa y seguir las instrucciones que se muestran en pantalla.

------------

PROPÓSITO DE LA APLICACIÓN:

La aplicación consiste en una plataforma de compra y venta de claves para diferentes programas de software. Todos los procedimientos se realizan de forma segura mediante cifrado y descifrado de datos sensibles, tratamiento de contraseñas con funciones resumen y tiempos de espera entre acciones. En caso de ataque y robo de la información de la base de datos (registros.json en nuestro caso), el atacante no podrá acceder a datos sensibles ya que están cifrados de forma adecuada de modo que el atacante no posee la clave de cifrado y descifrado para acceder a los datos. Esto último sucede ya que la clave de cifrado y descifrado para cada usuario se realiza mediante derivación de clave usando la contraseña del usuario en cuestión en su forma hash.

------------

COSAS A CONSIDERAR:

- Las cantidades de dinero tienen que ser escritas utilizando punto ('.') como separador para los decimales (formato inglés) debido al tratamiento de los floats en el lenguaje Python.
- La aplicación contiene tiempos de espera entre acciones para prevenir al atacante de realizar operaciones de fuerza bruta y forzar la aplicación para alterar su funcionamiento normal.
- Para la mayoría de menús, se puede pulsar la tecla '0' para volver hacia atrás.
- En caso de error al rellenar formularios, se mostrarán los requisitos del campo concreto.
- Para esta versión de la aplicación, el usuario puede ingresar dinero en su cuenta de manera infinita sin usar los datos bancarios para hacer la ejecución de la misma más simple.
