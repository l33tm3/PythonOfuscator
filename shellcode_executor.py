import ctypes
import argparse
import sys

# Definiciones de constantes de la API de Windows para mayor claridad.
MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40
INFINITE = -1

def check_windows():
    """
    Verifica si el sistema operativo es Windows.
    Si no lo es, termina el script con un error.
    """
    if sys.platform != "win32":
        print("Error: Este script está diseñado para ejecutarse solo en Windows.")
        sys.exit(1)

def setup_kernel32_functions():
    """
    Configura y devuelve las funciones de kernel32.dll con los tipos correctos.
    Esto mejora la robustez y la compatibilidad entre 32 y 64 bits.
    """
    kernel32 = ctypes.windll.kernel32

    # VirtualAlloc: Reserva o confirma un bloque de páginas en el espacio de direcciones virtuales del proceso que llama.
    # https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualalloc
    kernel32.VirtualAlloc.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_uint, ctypes.c_uint]
    kernel32.VirtualAlloc.restype = ctypes.c_void_p

    # RtlMoveMemory: Copia el contenido de un bloque de memoria a otro.
    # https://docs.microsoft.com/en-us/windows/win32/devnotes/rtlmovememory
    kernel32.RtlMoveMemory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t]
    kernel32.RtlMoveMemory.restype = None

    # CreateThread: Crea un hilo que se ejecutará dentro del espacio de direcciones virtuales del proceso que llama.
    # https://docs.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createthread
    kernel32.CreateThread.argtypes = [ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]
    kernel32.CreateThread.restype = ctypes.c_void_p

    # WaitForSingleObject: Espera hasta que el objeto especificado esté en estado señalado o hasta que expire el intervalo de tiempo.
    # https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject
    kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_uint]
    kernel32.WaitForSingleObject.restype = ctypes.c_uint

    return kernel32

def parse_args():
    """
    Analiza los argumentos de la línea de comandos.
    """
    parser = argparse.ArgumentParser(description="Ejecutor de Shellcode en Windows usando ctypes.")
    parser.add_argument("-i", "--input", help="Ruta al archivo de shellcode binario.", type=argparse.FileType('rb'), required=True)
    return parser.parse_args()

def allocate_and_execute_shellcode(kernel32, shellcode):
    """
    Asigna memoria, copia el shellcode y lo ejecuta en un nuevo hilo.
    """
    # 1. Asignar memoria con permisos de lectura, escritura y ejecución.
    ptr = kernel32.VirtualAlloc(None, len(shellcode), MEM_COMMIT, PAGE_EXECUTE_READWRITE)
    if not ptr:
        raise RuntimeError(f"Error al asignar memoria: {ctypes.get_last_error()}")

    print(f"Memoria asignada en la dirección: 0x{ptr:016X}")

    # 2. Copiar el shellcode a la memoria asignada.
    shellcode_buffer = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
    kernel32.RtlMoveMemory(ptr, shellcode_buffer, len(shellcode))

    print("Shellcode copiado a la memoria.")

    # 3. Crear un nuevo hilo para ejecutar el shellcode.
    thread_handle = kernel32.CreateThread(None, 0, ptr, None, 0, None)
    if not thread_handle:
        raise RuntimeError(f"Error al crear el hilo: {ctypes.get_last_error()}")

    print(f"Hilo creado con handle: 0x{thread_handle:016X}. Esperando a que termine...")

    # 4. Esperar a que el hilo termine su ejecución.
    kernel32.WaitForSingleObject(thread_handle, INFINITE)

    print("El hilo del shellcode ha terminado.")

def main():
    """
    Función principal del script.
    """
    check_windows()
    kernel32 = setup_kernel32_functions()

    try:
        args = parse_args()
        with args.input as f:
            shellcode = f.read()

        if not shellcode:
            print("Error: El archivo de shellcode está vacío.")
            return

        print(f"Leídos {len(shellcode)} bytes de shellcode desde '{args.input.name}'.")
        allocate_and_execute_shellcode(kernel32, shellcode)

    except FileNotFoundError as e:
        # Este error es manejado por argparse.FileType, pero se mantiene por si acaso.
        print(f"Error: Archivo no encontrado. Detalles: {e}")
    except RuntimeError as e:
        print(f"Error en tiempo de ejecución de la API de Windows: {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado. Detalles: {e}")

if __name__ == '__main__':
    main()