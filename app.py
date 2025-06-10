from flask import Flask, render_template, request, redirect
from load_data import carregar_estructura, carregar_sabers
from utils import generar_docx
import os
import json
import uuid
import time

app = Flask(__name__)

estructura = carregar_estructura('competencies.csv')
sabers_data = carregar_sabers('sabers.csv')

TEMP_DIR = 'static/'
FILE_TTL = 3600  # Temps de vida dels fitxers en segons (ex: 1 hora)

def netejar_fitxers_temporals():
    now = time.time()
    for fitxer in os.listdir(TEMP_DIR):
        if fitxer.startswith('informe_') and fitxer.endswith('.docx'):
            ruta_fitxer = os.path.join(TEMP_DIR, fitxer)
            if os.path.isfile(ruta_fitxer) and now - os.path.getmtime(ruta_fitxer) > FILE_TTL:
                try:
                    os.remove(ruta_fitxer)
                except Exception as e:
                    print(f"Error eliminant fitxer temporal {fitxer}: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    netejar_fitxers_temporals()
    nivells = list(estructura.keys())
    if request.method == 'POST':
        nivell = request.form['nivell']
        return redirect(f'/formulari?nivell={nivell}')
    return render_template('index.html', nivells=nivells)

@app.route('/formulari', methods=['GET', 'POST'])
def formulari():
    global estructura, sabers_data
    nivell = request.args.get('nivell')
    cursos = list(estructura[nivell].keys())
    estructura_json = estructura[nivell]
    sabers_json = sabers_data[nivell]

    if request.method == 'POST':
        dades = {
            'nivell': request.form['nivell'],
            'curs': request.form['curs'],
            'materia': request.form['materia'],
            'competencies': request.form.getlist('competencies'),
            'criteris': request.form.getlist('criteris'),
            'sabers': request.form.getlist('sabers')
        }
        nom_fitxer = f"static/informe_{uuid.uuid4()}.docx"
        generar_docx(dades, nom_fitxer)
        return render_template('resultat.html', dades=dades, doc=nom_fitxer)

    return render_template('formulari.html',
                           nivell=nivell,
                           cursos=cursos,
                           estructura=estructura[nivell],
                           estructura_json=json.dumps(estructura[nivell], ensure_ascii=False),
                           sabers_json=json.dumps(sabers_data[nivell], ensure_ascii=False))

if __name__ == '__main__':
    app.run(debug=True)
