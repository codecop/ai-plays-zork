# PyFrotz

[PyFrotz](https://github.com/HelloChatterbox/pyFrotz), a Python wrapper around [frotz](https://gitlab.com/DavidGriffith/frotz). Frotz is an Infocom interpreter by Stefan Jokisch and now maintained by David Griffith. Conforms to Z-Machine Standard 1.0 and supports V1-V6 and V7/V8 games.

## Dfrotz - Dumb Frotz

Dumb Frotz is a command-line interpreter that uses standard input and output, version 2.44.

[dfrotz' Man Page](https://www.mankier.com/6/dfrotz)

## Install under Linux

install the python package from pip as usual

```bash
pip install pyfrotz
```

which will in turn compile and install `dfrotz`.

## Install under Windows

Get `dfrotz`, compiled for Windows by Hugo Labrande, from [IF Archive](https://www.ifarchive.org/indexes/if-archive/infocom/interpreters/frotz/) and copy `dfrotz.exe` to `~/.pyfrotz`.

modify `pyFrotz-0.1.5/setup.py` to skip compilation and install manually using

```bash
pip install frotz\pyFrotz-0.1.5
```
