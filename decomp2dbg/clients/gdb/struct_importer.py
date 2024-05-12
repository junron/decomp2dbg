from ...utils import *
from .utils import *
import tempfile
import os

class StructImporter:
    __slots__ = (
        '_gcc',
    )

    def __init__(self):
        self._gcc = None

    def check_native_symbol_support(self):
        # validate binutils bins exist
        try:
            self._gcc = which("gcc")
        except FileNotFoundError as e:
            err(f"Binutils binaries not found: {e}")
            return False

        return True

    def import_struct(self, structs_string: str):
        if not self.check_native_symbol_support():
            err("Native struct support not supported on this platform.")
            info("If you are on Linux and want native struct support make sure you have gcc.")
            return False
    
        fd, filename = tempfile.mkstemp(dir="/tmp", suffix=".c")
        symbols_filename = filename[:-2]

        
        f = open(filename, "w")
        f.write(structs_string)
        f.close()
        os.system(f"{self._gcc} -g -c -fno-eliminate-unused-debug-types {filename} -o {symbols_filename}")

        gdb.execute(f"add-symbol-file {symbols_filename}", to_string=True)
        os.unlink(symbols_filename)
        os.unlink(filename)


