# Ejecutor de Shellcode en Python para Windows

## Descripción

Este proyecto es un script de Python diseñado para cargar y ejecutar shellcode desde un archivo binario en un entorno de Windows. Utiliza la biblioteca `ctypes` para interactuar directamente con la API de Windows, lo que le permite asignar memoria ejecutable, copiar el shellcode y ejecutarlo en un nuevo hilo.

Este script es una herramienta útil para investigadores de seguridad, pentesters y desarrolladores que necesitan una forma rápida y sencilla de probar shellcode en un entorno controlado.

## Características

- **Carga de Shellcode**: Carga shellcode desde un archivo binario especificado.
- **Ejecución Segura**: Utiliza funciones de la API de Windows (`VirtualAlloc`, `CreateThread`) para una ejecución robusta.
- **Compatibilidad**: Funciona en versiones de 32 y 64 bits de Windows gracias al uso de tipos de datos correctos en `ctypes`.
- **Comprobación del SO**: Verifica que el script se esté ejecutando en Windows para evitar errores en otros sistemas operativos.
- **Manejo de Errores**: Incluye un manejo de errores claro para fallos en la asignación de memoria o creación de hilos.
- **Uso Sencillo**: Interfaz de línea de comandos simple para una fácil ejecución.

## Requisitos

- Python 3.x
- Sistema operativo Windows

## Uso

1.  Clona este repositorio o descarga el código fuente.
2.  Asegúrate de tener Python 3.x instalado en tu sistema.
3.  Ejecuta el script desde la línea de comandos, proporcionando la ruta al archivo de shellcode que deseas ejecutar.

    ```bash
    python shellcode_executor.py -i ruta/al/shellcode.bin
    ```

    Reemplaza `ruta/al/shellcode.bin` con la ruta real de tu archivo.

## ⚠️ Advertencia de Seguridad

La ejecución de shellcode es inherentemente peligrosa y solo debe realizarse con código de fuentes confiables y con fines de investigación o pruebas autorizadas. Ejecutar shellcode desconocido o malicioso puede comprometer la seguridad de tu sistema. **Úsalo con extrema precaución.**

## Contribuciones

Las contribuciones son bienvenidas. Si tienes ideas para mejorar este proyecto, no dudes en abrir un *issue* o enviar un *pull request*.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más detalles.
