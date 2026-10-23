#!/usr/bin/env python3
"""
Renombrador masivo - v2 (limpiar nombres, con recursivo opcional)

Limpia los nombres de los archivos de una carpeta para que sean "sanos":
sin espacios, sin acentos, sin mayusculas raras, sin caracteres molestos.
    "Mi Archivo (1).PDF"  ->  "mi_archivo_1.pdf"

Por defecto corre en modo PRUEBA (no renombra, solo muestra) y SOLO en la
carpeta indicada (no entra a subcarpetas). Con --recursivo tambien entra a
las subcarpetas; con --aplicar renombra de verdad.

OJO con --recursivo: si tenés proyectos, webs o codigo donde un archivo
hace referencia a otro por su nombre, renombrarlos puede romper esos links.
Usá recursivo solo en carpetas "sueltas" (fotos, documentos), no en codigo.

Uso:
    python3 renombrador.py                        # prueba, ~/Descargas, sin subcarpetas
    python3 renombrador.py ~/fotos                # prueba sobre ~/fotos
    python3 renombrador.py ~/fotos --recursivo    # prueba, incluye subcarpetas
    python3 renombrador.py ~/fotos -r -a          # recursivo y aplicando
"""

import re
import sys
import unicodedata
import argparse
from pathlib import Path


def parsear_args():
    p = argparse.ArgumentParser(
        description="Limpia los nombres de archivos: sin espacios, acentos ni caracteres raros."
    )
    p.add_argument("carpeta", nargs="?", default=str(Path.home() / "Descargas"),
                   help="carpeta cuyos archivos renombrar (default: ~/Descargas)")
    p.add_argument("-a", "--aplicar", action="store_true",
                   help="renombrar de verdad (sin esto, solo muestra que haria)")
    p.add_argument("-r", "--recursivo", action="store_true",
                   help="entrar tambien a las subcarpetas (con cuidado, ver aviso)")
    return p.parse_args()


def limpiar(nombre):
    """Convierte un nombre de archivo en una version limpia, respetando la extension."""
    base, punto, ext = nombre.rpartition(".")
    if not punto:
        base, ext = nombre, ""

    # Sacar acentos: descompone la letra acentuada y tira la marca del acento
    base = unicodedata.normalize("NFKD", base)
    base = base.encode("ascii", "ignore").decode("ascii")
    base = base.lower()
    # Todo lo que no sea letra/numero -> guion bajo
    base = re.sub(r"[^a-z0-9]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")

    if not base:
        base = "archivo"

    return f"{base}.{ext.lower()}" if ext else base


def destino_sin_pisar(carpeta, nombre):
    """Si ya existe ese nombre en la carpeta, agrega un numero para no pisar."""
    if not (carpeta / nombre).exists():
        return carpeta / nombre
    base, punto, ext = nombre.rpartition(".")
    if not punto:
        base, ext = nombre, ""
    n = 1
    while True:
        candidato = f"{base}_{n}.{ext}" if ext else f"{base}_{n}"
        if not (carpeta / candidato).exists():
            return carpeta / candidato
        n += 1


def archivos_a_procesar(base, recursivo):
    """Devuelve los archivos a mirar: solo la carpeta, o tambien subcarpetas."""
    patron = base.rglob("*") if recursivo else base.iterdir()
    for ruta in patron:
        if ruta.is_file() and not ruta.name.startswith("."):
            yield ruta


def main():
    args = parsear_args()
    base = Path(args.carpeta).expanduser()

    if not base.is_dir():
        print(f"No existe la carpeta: {base}")
        return

    modo = "APLICANDO (renombra de verdad)" if args.aplicar else "PRUEBA (no renombra nada)"
    alcance = "carpeta y subcarpetas" if args.recursivo else "solo esta carpeta"
    print(f"Carpeta: {base}")
    print(f"Modo: {modo}  |  Alcance: {alcance}\n")

    cambios = 0
    for archivo in archivos_a_procesar(base, args.recursivo):
        nuevo = limpiar(archivo.name)
        if nuevo == archivo.name:
            continue                        # ya estaba limpio

        # El renombre es DENTRO de la misma carpeta del archivo (no lo movemos)
        destino = destino_sin_pisar(archivo.parent, nuevo)

        # Mostramos la ruta relativa para ubicarse cuando es recursivo
        try:
            rel = archivo.relative_to(base)
        except ValueError:
            rel = archivo.name
        print(f"  {rel}")
        print(f"      ->  {destino.name}")

        if args.aplicar:
            archivo.rename(destino)

        cambios += 1

    print()
    if cambios == 0:
        print("Todos los nombres ya estaban limpios. Nada que renombrar.")
    elif args.aplicar:
        print(f"Listo. {cambios} archivo(s) renombrado(s).")
    else:
        print(f"{cambios} archivo(s) se renombrarian. Corré con --aplicar para hacerlo.")


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        # Pasa cuando cortás la salida con 'head' o '| less': no es un error real.
        # Cerramos stdout en silencio para terminar limpio.
        try:
            sys.stdout.close()
        except Exception:
            pass
