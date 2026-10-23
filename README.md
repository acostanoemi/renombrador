# renombrador

Script de Python que limpia los nombres de los archivos de una carpeta: les saca espacios, acentos, mayúsculas y caracteres raros.

```
Mi Archivo (1).PDF   ->   mi_archivo_1.pdf
Canción Favorita.MP3 ->   cancion_favorita.mp3
```

## Para qué sirve

Los nombres con espacios, acentos y paréntesis dan problemas en la terminal, en la web, en scripts y al pasar archivos entre sistemas (Linux, Windows, un servidor). Nombres limpios (minúsculas, sin acentos, con guiones bajos) se manejan sin dolores de cabeza.

## Lo importante: corre en modo prueba primero

Por defecto **no renombra nada**: te muestra qué haría. Recién con `--aplicar` renombra de verdad. Y por defecto **solo mira la carpeta indicada**, sin entrar a subcarpetas.

## Cuidado con `--recursivo`

Con `--recursivo` también entra a las subcarpetas. Pero si tenés proyectos, páginas web o código donde un archivo hace referencia a otro por su nombre, renombrarlos puede romper esos links. Usalo solo en carpetas "sueltas" (fotos, documentos), nunca sobre código.

## Qué tiene en cuenta

- Respeta la extensión (y la pasa a minúscula: `.PDF` → `.pdf`).
- **No pisa archivos:** si el nombre limpio ya existe, agrega un número.
- **No toca** archivos que ya tengan el nombre limpio, ni carpetas, ni ocultos.

## Requisitos

Solo Python 3. No usa librerías externas.

## Uso

```bash
python3 renombrador.py                        # prueba, ~/Descargas, sin subcarpetas
python3 renombrador.py ~/fotos                # prueba sobre ~/fotos
python3 renombrador.py ~/fotos --recursivo    # prueba, incluye subcarpetas
python3 renombrador.py ~/fotos -r -a          # recursivo y aplicando
```

| Opción | Qué hace |
|--------|----------|
| `carpeta` | Carpeta cuyos archivos renombrar (default: `~/Descargas`) |
| `-a`, `--aplicar` | Renombrar de verdad (sin esto, solo muestra qué haría) |
| `-r`, `--recursivo` | Entrar también a las subcarpetas (ver aviso de arriba) |

## Roadmap

- [x] v1: limpiar nombres (espacios, acentos, mayúsculas, caracteres raros)
- [x] v2: opción recursiva para entrar a subcarpetas
- [ ] v3: reemplazar un texto por otro en los nombres
- [ ] v4: numerar en secuencia (foto_01, foto_02...)
