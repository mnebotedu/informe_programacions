
from flask import Flask, render_template, request, redirect
from load_data import carregar_estructura, carregar_sabers
from utils import generar_docx
import os
import json

app = Flask(__name__)

estructura = carregar_estructura('competencies.csv')
sabers_data = carregar_sabers('sabers.csv')

@app.route('/', methods=['GET', 'POST'])
def index():
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
        nom_fitxer = 'static/informe.docx'
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
