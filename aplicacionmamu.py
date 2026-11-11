from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget,QPushButton, QLabel, QVBoxLayout, QCalendarWidget, QListWidget, QHBoxLayout, QLineEdit
from random import randint
import json
import os
app = QApplication([])
app.setQuitOnLastWindowClosed(False)
main_win = QWidget()
main_win.setWindowTitle('Agenda Martus')
main_win.resize(600, 600)
# Segunda ventana (Calendario)
segundaventana = QWidget()
segundaventana.setWindowTitle('Calendario')
segundaventana.resize(800, 500)
# Primera ventana widgets
but = QPushButton('Iniciar')
text = QLabel("¡Buenos días!, Comencemos con una buena organización :)")
line = QVBoxLayout()
line.addWidget(text, alignment = Qt.AlignCenter)
line.addWidget(but, alignment = Qt.AlignCenter)
main_win.setLayout(line)
#Segunda ventana widgets
text2 = QLabel("Calendario")
calendar = QCalendarWidget()
layout2 = QVBoxLayout()
layout2.addWidget(text2, alignment = Qt.AlignCenter)
layout2.addWidget(calendar)
segundaventana.setLayout(layout2)
# Tercera ventana
terceraventana = QWidget()
terceraventana.setWindowTitle("Horarios del día ⭐")
terceraventana.resize(500, 700)


layout3 = QVBoxLayout()
label_fecha = QLabel("Fecha selecionada")
label_horarios = QLabel("Horarios:")
layout3.addWidget(label_fecha, alignment = Qt.AlignCenter)
layout3.addWidget(label_horarios, alignment = Qt.AlignCenter)
terceraventana.setLayout(layout3)

# Horarios de las fechas

class VentanaHorarios(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Horarios del día ⭐")
        self.resize(500, 700)
        layout = QVBoxLayout()
        self.label_fecha = QLabel('Fecha seleccionada:')
        self.label_fecha.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_fecha)

        self.layout_horarios = QVBoxLayout()
        horas = ['07:00', '07:30', '08:00', '08:30', '09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00','20:30', '21:00', '21:30', '22:00']
        self.inputs_horarios = {}
        for hora in horas:
            fila_layout = QHBoxLayout()
            lbl_hora = QLabel(hora)
            lbl_hora.setFixedWidth(60)
            fila_layout = QHBoxLayout()
            txt_nota = QLineEdit()
            txt_nota.setPlaceholderText("Escribir tareas para las " + hora + "...")
            self.inputs_horarios[hora] = txt_nota
            fila_layout.addWidget(lbl_hora)
            fila_layout.addWidget(txt_nota)
            self.layout_horarios.addLayout(fila_layout)
        layout.addLayout(self.layout_horarios) 
        self.boton_guardar = QPushButton('Guardar notas')
        self.boton_guardar.clicked.connect(self.guardar_datos)
        layout.addWidget(self.boton_guardar, alignment=Qt.AlignCenter)
        self.boton_cerrar = QPushButton('Cerrar')
        self.boton_cerrar.clicked.connect(self.close)
        layout.addWidget(self.boton_cerrar, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    def guardar_datos(self):
        try:
            datos = {}
            if os.path.exists("agenda.json"):
                with open("agenda.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
            
            # Por si la fecha no llegó a cargarse bien antes de apretar el botón
            if not hasattr(self, 'fecha_actual') or not self.fecha_actual:
                self.fecha_actual = "Fecha_General"

            notas_dia = {}
            for hora, txt in self.inputs_horarios.items():
                notas_dia[hora] = txt.text()
            
            datos[self.fecha_actual] = notas_dia
            
            with open("agenda.json", "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=4)
            
            # Ocultamos la ventana de horarios de forma limpia
            self.hide()
            
        except Exception as e:
            # Si algo falla, te avisa en pantalla en vez de cerrar la app
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Atención", f"No se pudo guardar: {str(e)}")

    def cargar_datos(self):
        for hora, txt in self.inputs_horarios.items():
            txt.clear()
        
        if os.path.exists("agenda.json"):
            try:
                with open("agenda.json", "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    if self.fecha_actual in datos:
                        notas_dia = datos[self.fecha_actual]
                        for hora, texto in notas_dia.items():
                            if hora in self.inputs_horarios:
                                self.inputs_horarios[hora].setText(texto)
            except:
                pass
    def actualizar_fecha(self, fecha):
        self.fecha_actual = fecha.toString("dd/MM/yyyy")
        self.label_fecha.setText('Fecha seleccionada: ' + self.fecha_actual)
        self.cargar_datos()


def abrir_horarios(fecha_clic):
    global ventana_horarios
    try:
        ventana_horarios.close()
    except:
        pass
    try:        
        ventana_horarios = VentanaHorarios()
        fecha = calendar.selectedDate()
        texto_fecha = "Fecha seleccionada: " + fecha_clic.toString("dd/MM/yyyy")
        ventana_horarios.label_fecha.setText(texto_fecha)
        ventana_horarios.show()
        ventana_horarios.raise_()
    except Exception as e:
        print('Error al abrir horarios;', e)
calendar.activated.connect(abrir_horarios)

def abrir():
    main_win.hide()
    segundaventana.show()

but.clicked.connect(abrir)

main_win.show()
app.exec_()