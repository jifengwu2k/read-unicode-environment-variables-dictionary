# encoding: utf-8
# Copyright (c) 2025 Jifeng Wu
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
import ctypes
import re

from posix_or_nt import posix_or_nt
from typing import Dict, Text

# Removes environment variables like `u'=::=::\\'`
NAME_VALUE_PATTERN = re.compile(u'^([^\\s=]+)=(.*)$')

if posix_or_nt() == 'nt':
    import ctypes.wintypes

    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    GetEnvironmentStringsW = kernel32.GetEnvironmentStringsW
    GetEnvironmentStringsW.restype = ctypes.c_void_p

    FreeEnvironmentStringsW = kernel32.FreeEnvironmentStringsW
    FreeEnvironmentStringsW.argtypes = [ctypes.c_void_p]
    FreeEnvironmentStringsW.restype = ctypes.wintypes.BOOL


    def read_unicode_environment_variables_dictionary():
        # type: () -> Dict[Text, Text]
        """
        Use raw ctypes to read Unicode environment variables directly from the OS, even where Python's own `os` module is incomplete or restricted.

        - Never uses the `os` module.
        - All names and values are Unicode, even on Python 2.
        - Returns a deep copy. Modifying the dictionary is safe: it will never affect your process environment.
        """
        env_block_addr = GetEnvironmentStringsW()
        if not env_block_addr:
            raise ctypes.WinError(ctypes.get_last_error())

        environment_variables_dictionary = {}

        cur_addr = env_block_addr
        while True:
            # Convert address to LPWSTR (`wchar_t *`)
            lpwstr = ctypes.cast(cur_addr, ctypes.c_wchar_p)

            # Get Unicode string
            entry = lpwstr.value

            if not entry:
                break

            match_or_none = NAME_VALUE_PATTERN.match(entry)
            if match_or_none is not None:
                name = match_or_none.group(1).upper()
                value = match_or_none.group(2)
                environment_variables_dictionary[name] = value

            # Move address forward, +1 for the trailing L'\0'`
            cur_addr += ctypes.sizeof(ctypes.c_wchar) * (len(entry) + 1)

        FreeEnvironmentStringsW(env_block_addr)

        return environment_variables_dictionary
else:
    # Load libc of current process
    libc = ctypes.CDLL(None, use_errno=True)


    def read_unicode_environment_variables_dictionary():
        # type: () -> Dict[Text, Text]
        """
        Use raw ctypes to read Unicode environment variables directly from the OS, even where Python's own `os` module is incomplete or restricted.

        - Never uses the `os` module.
        - All names and values are Unicode, even on Python 2.
        - Returns a deep copy. Modifying the dictionary is safe: it will never affect your process environment.
        """
        environ = ctypes.POINTER(ctypes.c_char_p).in_dll(libc, "environ")

        environment_variables_dictionary = {}

        i = 0
        while environ[i]:
            entry = environ[i].decode('utf-8')

            match_or_none = NAME_VALUE_PATTERN.match(entry)
            if match_or_none is not None:
                name = match_or_none.group(1)
                value = match_or_none.group(2)
                environment_variables_dictionary[name] = value

            i += 1

        return environment_variables_dictionary
