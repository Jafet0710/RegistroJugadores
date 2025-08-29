from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import io

app = Flask(__name__)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Resumen Asistencia U13', ln=True, align='C')
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(60, 10, 'Jugador', border=1, fill=True)
        self.cell(40, 10, 'Asistencias', border=1, fill=True)
        self.cell(40, 10, 'Porcentaje', border=1, fill=True)
        self.cell(40, 10, 'Nivel', border=1, fill=True)
        self.ln()

    def fila_jugador(self, nombre, asistencias, total, porcentaje):
        self.set_font('Arial', '', 11)
        self.set_text_color(0, 0, 0)
        self.cell(60, 10, nombre, border=1)
        self.cell(40, 10, f"{asistencias}/{total}", border=1)
        self.cell(40, 10, f"{porcentaje:.1f}%", border=1)

       
        if porcentaje >= 95:
            self.set_text_color(0, 128, 0) 
            nivel = "Alto"
        elif porcentaje >= 50:
            self.set_text_color(255, 165, 0)  
            nivel = "Medio"
        else:
            self.set_text_color(255, 0, 0) 
            nivel = "Bajo"

        self.cell(40, 10, nivel, border=1)
        self.set_text_color(0, 0, 0)  
        self.ln()

@app.route('/', methods=['GET', 'POST'])
def index():
    jugadores = [
        "Andrés Ramírez", "Carlos Machado", "Yeltsin Otárola", "Damián Chaves",
        "Valentina Chinchilla", "Danny Madriz", "Dylan Cortes", "Dylan Ramírez",
        "Dylan Alvarado", "Evan Guevara", "Eydan Ramírez", "Gabriel Barquero",
        "Ismael Solano", "Joan Solano", "José Torrez", "José Luis Roque",
        "Juan Pablo Víquez", "Luis Felipe Fallas"
    ]
    total = 8

    if request.method == 'POST':
        asistencias = {}
        for jugador in jugadores:
            asistencias_jugador = int(request.form.get(jugador, 0))
            porcentaje = (asistencias_jugador / total) * 100
            asistencias[jugador] = (asistencias_jugador, porcentaje)

        pdf = PDF()
        pdf.add_page()
        for nombre, (asistencias_realizadas, porcentaje) in asistencias.items():
            pdf.fila_jugador(nombre, asistencias_realizadas, total, porcentaje)

        pdf_bytes = pdf.output(dest='S').encode('latin1')
        buffer = io.BytesIO(pdf_bytes)
        return send_file(buffer, as_attachment=True, download_name="asistencia_U13.pdf", mimetype='application/pdf')


    return render_template('index.html', jugadores=jugadores)

if __name__ == '__main__':
    app.run(debug=True)
