# `read-unicode-environment-variables-dictionary`

> Use raw ctypes to read Unicode environment variables directly from the OS, even where Python's own `os` module is
> incomplete or restricted.

## Modern Python, Real Environment

The traditional `os` module in Python keeps you at arm's length from the operating system - especially on unusual
platforms (think Android and iOS). Sometimes, that means missing features, incomplete access, or just plain
*frustration*.

**read-environment-variables-dictionary** is the essential building block for serious system scripting and tooling:

- **Bypasses the `os` module entirely.**
- Accesses the *actual* process environment directly through `ctypes`, using POSIX and Win32 APIs - no wrappers, no
  middlemen, no artificial restrictions.
- Fully Unicode - even fixes Python 2's legacy handling.

If you're creating tools, build systems, cross-platform utilities, deployment scripts, or Python-based automation, *
*this is the reliable, lowest-level method for reading the environment.** Use it directly, or build on top of it.

## Usage

```python
# coding=utf-8
from __future__ import print_function

from read_unicode_environment_variables_dictionary import read_unicode_environment_variables_dictionary

env = read_unicode_environment_variables_dictionary()
print(env[u'PATH'])
```

## Install

```bash
pip install read-unicode-environment-variables-dictionary
```

## Contributing

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).