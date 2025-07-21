import sys
import gdown
from pathlib import Path
from PySide6.QtWidgets import QApplication
from menu_principal import MenuPrincipal

# ID del archivo en Google Drive (¡reemplaza por el tuyo!)
GOOGLE_DRIVE_ID = "14U2SIUrCD7iFV-sLD4X301zPsuBYGnt_"

def descargar_db_desde_drive():
    output_path = Path(__file__).resolve().parent.parent / "db" / "EMP.db"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}"
    print("⬇️ Descargando base de datos desde Google Drive...")

    try:
        gdown.download(url, str(output_path), quiet=False)
        print("✅ Base de datos descargada correctamente en:", output_path)
    except Exception as e:
        print("❌ Error al descargar la base de datos:", e)

if __name__ == "__main__":
    descargar_db_desde_drive()

    app = QApplication(sys.argv)
    ventana = MenuPrincipal(app)
    ventana.show()
    sys.exit(app.exec())