from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QRadioButton, 
    QSizePolicy, QGridLayout, QLineEdit, QSpacerItem, QGroupBox, QDateEdit, QTextEdit, QFrame
)
from PySide6.QtGui import QIcon, QPixmap, QPainter

from PySide6.QtCore import Qt

import darkdetect

import sys

from pathlib import Path

class login(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        if darkdetect.isDark():
         modo = "oscuro"
       
        else:
         modo = "claro"

        if darkdetect.isDark():
         app.setStyleSheet("""
            QLineEdit, {
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

        titulo1 = QLabel("Bienvenido")
        titulo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo1.setStyleSheet("font-weight: regular; font-size: 16px")
        self.layout_principal.addWidget(titulo1)
        

        titulo2 = QLabel("al")
        titulo2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo2.setStyleSheet("font-weight: regular; font-size: 16px")
        self.layout_principal.addWidget(titulo2)
        

        titulo3 = QLabel("Sistema de Administración de Emplazamientos")
        titulo3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo3.setStyleSheet("font-weight: regular; font-size: 16px")
        self.layout_principal.addWidget(titulo3)
        

        self.layout_principal.addSpacerItem(QSpacerItem(10, 50, QSizePolicy.Preferred, QSizePolicy.Preferred))


        # Frame Central
        self.frame_central = QFrame()
        self.datos_layout = QGridLayout()
        self.frame_central.setLayout(self.datos_layout)
        self.datos_layout.setSpacing(10)
        self.usuario = QLineEdit()        
        self.datos_layout.addWidget(QLabel("Usuario"), 1, 0)
        self.datos_layout.addWidget(self.usuario, 2, 0)
        self.usuario.setFixedWidth(150)
        self.layout_principal.addWidget(self.frame_central)
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.datos_layout.addWidget(QLabel("Password"), 4, 0)
        self.datos_layout.addWidget(self.password, 5, 0)
        self.password.setFixedWidth(150)
        
        self.login_btn = QPushButton("Iniciar Sesion")
        self.login_btn.setFixedSize(150, 20)
        self.guess_btn = QPushButton("Continuar como invitado")
        self.guess_btn.setFixedSize(150, 20)
        self.datos_layout.addWidget(self.login_btn, 7, 0)
    
        self.datos_layout.addWidget(self.guess_btn, 8, 0)





        

        

            
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = login()
    ventana.setWindowTitle("Iniciar Sesion")    
    base_dir = Path(__file__).resolve().parent
    icono_ventana = base_dir.parent / "assets" / "login icon.ico"    
    ventana.setWindowIcon(QIcon(str(icono_ventana)))    
    ventana.show()
    sys.exit(app.exec())