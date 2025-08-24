from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QSizePolicy, QGridLayout, QLineEdit, QSpacerItem, QFrame, QMessageBox
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QIntValidator, QGuiApplication
from PySide6.QtCore import Qt, Signal
import darkdetect
import sys
from pathlib import Path
from nuevo_registro import UI_Nuevo

class login_nuevoUI(QWidget):
    auth_ok = Signal()
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app        
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)

        base_dir = Path(__file__).resolve().parent
        self.assets = base_dir.parent / "assets" 
        
        if darkdetect.isDark():
         modo = "oscuro"
       
        else:
         modo = "claro"

        if darkdetect.isDark():
         app.setStyleSheet("""
            QLineEdit {
            background-color: #2e2e2e;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 5px;
              }
                QPushButton:pressed {
                 padding-right: 2px;
                 padding-bottom: 2px;
                 border: 1px inset gray;
                  }
                
             """)
        else:
            app.setStyleSheet("""
            QLineEdit, QPushButton {
            background-color: #eceff1;
            color: #000000;
            border: 1px solid #ccc;
            border-radius: 5px;
                }
                  QPushButton:pressed {
                    padding-right: 2px;
                    padding-bottom: 2px;
                    border: 1px inset gray;
        }
            """)
        # Layout Principal
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setAlignment(Qt.AlignTop)

        # Frame Superior
        self.frame_sup = QFrame()
        self.layout_sup = QHBoxLayout()
        self.frame_sup.setLayout(self.layout_sup)
        self.layout_principal.addWidget(self.frame_sup)
        self.layout_sup.setAlignment(Qt.AlignHCenter)

        titulo1 = QLabel("INICIA SESIÓN")
        titulo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo1.setStyleSheet("font-weight: regular; font-size: 16px")
        self.layout_principal.addWidget(titulo1)  
        

        #titulo2 = QLabel("Inicia sesión")
        #titulo2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #titulo2.setStyleSheet("font-weight: regular; font-size: 16px")
        #self.layout_principal.addWidget(titulo2)  
        self.layout_principal.addSpacerItem(QSpacerItem(10, 50, QSizePolicy.Preferred, QSizePolicy.Preferred))

       
        # Imagen de Login

        base_dir = Path(__file__).resolve().parent
        assets = base_dir.parent / "assets"

        self.imagen_usuario = QLabel()
        self.imagen_usuario.setFixedSize(170, 170)
        self.imagen_usuario.setScaledContents(True)
        self.layout_principal.addWidget(self.imagen_usuario, alignment=Qt.AlignCenter)
        self.imagen_usuario.setPixmap(QPixmap(str(assets / "user_image.png")))
        self.layout_principal.addSpacerItem(QSpacerItem(10, 50, QSizePolicy.Preferred, QSizePolicy.Preferred))
        



        # Frame Central
        self.frame_central = QFrame()
        self.datos_layout = QGridLayout()
        self.frame_central.setLayout(self.datos_layout)
        self.datos_layout.setSpacing(10)
        self.usuario = QLineEdit()
        self.usuario.setMaxLength(10)
        validator = QIntValidator(0, 999999999)
        self.usuario.setValidator(validator)
        self.datos_layout.addWidget(QLabel("Usuario"), 1, 0)
        self.datos_layout.addWidget(self.usuario, 2, 0)
        self.usuario.setFixedWidth(150)
        self.layout_principal.addWidget(self.frame_central)
        self.usuario.textChanged.connect(self._actualizar_avatar_por_usuario)
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.datos_layout.addWidget(QLabel("Password"), 4, 0)
        self.datos_layout.addWidget(self.password, 5, 0)
        self.password.setFixedWidth(150)
        self.password.returnPressed.connect(self.iniciar_sesion)
        
        
        self.login_btn = QPushButton("Iniciar Sesion")
        self.login_btn.setFixedSize(150, 35)
        self.login_btn.clicked.connect(self.iniciar_sesion)

        self.guess_btn = QPushButton("Continuar como invitado")
        self.guess_btn.setFixedSize(150, 20)
        self.datos_layout.addWidget(self.login_btn, 7, 0)    
        #self.datos_layout.addWidget(self.guess_btn, 8, 0)

    def _actualizar_avatar_por_usuario(self):
        user_id = self.usuario.text().strip()   # <- aquí usas self.usuario
        mapping = {
        "345838": "JJVE.png",
        "433086": "RRG.png",
        }
        img_path = self.assets / mapping.get(user_id, "user_image.png")
        self.imagen_usuario.setPixmap(QPixmap(str(img_path)))

    def iniciar_sesion(self):
        usuario = self.usuario.text()
        password = self.password.text()

        usuarios = {"345838": "camay", "433086": "Pemex123$"}

        if usuario in usuarios and usuarios[usuario] == password:
            #QMessageBox.information(self, "Bienvenido", f"Bienvenido")
            self.auth_ok.emit()
            self.close()
            #self.abrir_nuevo()
        else:
             QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.")

    #def abrir_nuevo(self):
        #self.ventana_nuevo = UI_Nuevo(self.app)
        #self.ventana_nuevo.show()   

        

            
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = login_nuevoUI(app)
    ventana.setWindowTitle("SAESF MADERO")    
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "login icon.ico"    
    ventana.setWindowIcon(QIcon(str(icono_ventana)))    
    ventana.show()

    screen = QGuiApplication.primaryScreen().availableGeometry()
    ventana.move(
        (screen.width() - ventana.width()) // 2,
        (screen.height() - ventana.height()) // 2
    )


    
    sys.exit(app.exec())