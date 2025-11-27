import os
import plistlib
from collections import Counter

DEVICES_DIR = "Devices"                    # o "Maker", como prefieras
OUTPUT_FILE = "cachebuilds_final.txt"


def normalizar_modelo(nombre_carpeta):
    """
    Convierte cualquier formato raro a iPhoneXX,Y estándar
    Ejemplos:
      iPhone17-4      → iPhone17,4
      iPhone17_4      → iPhone17,4
      iPhone 17,4     → iPhone17,4
      iPhone17,4      → iPhone17,4 (ya está bien)
    """
    if nombre_carpeta.startswith("iPhone"):
        # Quitamos "iPhone" y trabajamos con la parte numérica
        numero = nombre_carpeta[6:].strip()          # "17-4", "17_4", "17,4", etc.
        numero = numero.replace("-", ",").replace("_", ",")  # - y _ → ,
        numero = numero.replace(" ", "")               # espacios fuera
        return f"iPhone{numero}"
    return nombre_carpeta  # si no empieza con iPhone, lo dejamos igual


def extraer_cachebuild(ruta_plist):
    """Extrae CacheExtra → build de forma 100% fiable"""
    try:
        with open(ruta_plist, 'rb') as f:
            plist = plistlib.load(f, fmt=None)

        # Método actual (iOS 12+)
        cache_extra = plist.get("CacheExtra", {})
        if isinstance(cache_extra, dict):
            build = cache_extra.get("build")
            if build:
                return str(build).strip()

        # Casos muy antiguos
        for clave in ["CacheVersion", "CacheBuild", "BuildVersion"]:
            if clave in plist:
                return str(plist[clave]).strip()

        return None
    except:
        return None


def main():
    resultados = []  # (modelo_normalizado, build, archivo_origen)

    print("Procesando carpetas en:", DEVICES_DIR)
    print("-" * 80)

    for carpeta in sorted(os.listdir(DEVICES_DIR)):
        ruta_carpeta = os.path.join(DEVICES_DIR, carpeta)

        if not os.path.isdir(ruta_carpeta):
            continue

        # Normalizamos el nombre del modelo desde el nombre de la carpeta
        modelo = normalizar_modelo(carpeta)

        # Solo procesamos carpetas que parezcan de iPhone (opcional)
        if not modelo.startswith("iPhone"):
            continue

        # Buscar TODOS los MobileGestalt
        plists = [
            f for f in os.listdir(ruta_carpeta)
            if f.startswith("com.apple.MobileGestalt")
        ]

        if not plists:
            print(f"[NO FILE] {modelo:12} ← carpeta: {carpeta}")
            continue

        for archivo in plists:
            build = extraer_cachebuild(os.path.join(ruta_carpeta, archivo))
            if build:
                resultados.append((modelo, build, archivo))
                print(f"[OK] {modelo:12} = {build:10}  ← {archivo}  (carpeta: {carpeta})")
            else:
                print(f"[BAD] {modelo:12} = ???        ← {archivo} (sin build válido)")

    # Guardar TODOS los resultados con modelo normalizado
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("# Modelo normalizado → CacheBuild encontrado en cada archivo\n\n")
        for modelo, build, archivo in sorted(resultados):
            f.write(f'"{modelo}","{build}"\n')

    print("\n" + "="*80)
    print(f"Listo! {len(resultados)} CacheBuilds guardados en → {OUTPUT_FILE}")

    # Resumen por CacheBuild
    print("\nBuilds más comunes:")
    for build, cant in Counter([b for _,b,_ in resultados]).most_common():
        print(f"   {build} → {cant} veces")

    # Bonus: modelos únicos con sus builds (el último encontrado gana)
    print("\nModelos únicos (último build encontrado):")
    unicos = {}
    for m, b, _ in resultados:
        unicos[m] = b
    for m in sorted(unicos):
        print(f"{m} = {unicos[m]}")


if __name__ == "__main__":
    main()