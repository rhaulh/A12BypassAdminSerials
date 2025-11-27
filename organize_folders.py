import os
import plistlib
import shutil

# ----- Diccionario en el formato solicitado -----
ios_builds_dict = {
    "22H20": "18.7",
    "22H31": "18.7.1",
    "22F76": "18.5",
    "23A341": "26.0",
    "23A355": "26.0.1",
    "23B85": "26.1",
    "22D60": "18.3"
}

# ----- Carpeta base -----
BASE_DEVICES = "devices"


def organizar_gestalts():
    for model in os.listdir(BASE_DEVICES):
        model_path = os.path.join(BASE_DEVICES, model)

        if not os.path.isdir(model_path):
            continue

        gestalt_path = os.path.join(model_path, "com.apple.MobileGestalt.plist")

        if not os.path.exists(gestalt_path):
            print(f"[!] {model}: No tiene Gestalt.")
            continue

        try:
            with open(gestalt_path, "rb") as f:
                plist_data = plistlib.load(f)

            cache_version = plist_data.get("CacheVersion")

            if not cache_version:
                print(f"[!] {model}: No tiene CacheVersion.")
                continue

            if cache_version not in ios_builds_dict:
                print(f"[!] {model}: Build '{cache_version}' no reconocido.")
                continue

            # Ejemplo: "23B85" -> "26.1"
            ios_version_number = ios_builds_dict[cache_version]

            dest_folder = os.path.join(model_path, ios_version_number)
            os.makedirs(dest_folder, exist_ok=True)

            dest_file = os.path.join(dest_folder, "com.apple.MobileGestalt.plist")

            shutil.move(gestalt_path, dest_file)

            print(f"[OK] {model}: movido a {dest_folder}")

        except Exception as e:
            print(f"[ERROR] {model}: {e}")


if __name__ == "__main__":
    organizar_gestalts()
