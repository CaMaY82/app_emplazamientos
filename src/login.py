from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QSizePolicy, QGridLayout, QLineEdit, QSpacerItem, QFrame, QMessageBox
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QIntValidator, QGuiApplication
from PySide6.QtCore import Qt, Signal
import darkdetect
import sys
from pathlib import Path
from editar_registro import UI_editar

class loginUI(QWidget):
    auth_ok = Signal()
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app        
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
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

        titulo1 = QLabel("Sistema de Administración de Emplazamientos")
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
        
        user_img = QPixmap(base_dir.parent / "assets" / "user_image.png")
        user_img = base_dir.parent / "assets" / "user_image.png"
        
        imagen_usuario = QLabel()
        imagen_usuario.setFixedSize(150, 75)
        imagen_usuario.setScaledContents(True)
        
        pixmap = QPixmap(str(user_img))
        imagen_usuario.setPixmap(pixmap)

        self.layout_principal.addWidget(imagen_usuario, alignment=Qt.AlignCenter)
        imagen_usuario.setFixedSize(100, 100)

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
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.datos_layout.addWidget(QLabel("Password"), 4, 0)
        self.datos_layout.addWidget(self.password, 5, 0)
        self.password.setFixedWidth(150)
        self.password.returnPressed.connect(self.iniciar_sesion)
        
        
        self.login_btn = QPushButton("Iniciar Sesion")
        self.login_btn.setFixedSize(150, 20)
        self.login_btn.clicked.connect(self.iniciar_sesion)

        self.guess_btn = QPushButton("Continuar como invitado")
        self.guess_btn.setFixedSize(150, 20)
        self.datos_layout.addWidget(self.login_btn, 7, 0)    
        #self.datos_layout.addWidget(self.guess_btn, 8, 0)

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

    #def abrir_editar(self):
        #self.ventana_editar = UI_editar(self.app)
        #self.ventana_editar.show()

      

        

            
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = loginUI(app)
    ventana.setWindowTitle("Iniciar Sesion")    
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