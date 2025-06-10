from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def afegir_titol(doc, text):
    titol = doc.add_heading(text, 0)
    titol.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT


def afegir_encap1(doc, text):
    doc.add_heading(text, level=1)

def afegir_text(doc, text):
    doc.add_paragraph(text)


def afegir_llista(doc, elements):
    for el in elements:
        doc.add_paragraph(f"{el}", style='List Bullet')


def afegir_seccio_buida(doc, titol):
    doc.add_heading(titol, level=1)
    taula = doc.add_table(rows=1, cols=1)
    taula.style = 'Table Grid'
    taula.cell(0, 0).text = "\n\n\n"


def generar_docx(dades, nom_fitxer='informe.docx'):
    doc = Document()

    # Títol principal
    afegir_titol(doc, 'Esborrany de programació didàctica')


     # Informació bàsica com a llista
    info_basica = [
        f"Nivell educatiu: {dades['nivell']}",
        f"Curs: {dades['curs']}",
        f"Matèria: {dades['materia']}"
    ]
    afegir_llista(doc, info_basica)

    # Secció 1
    afegir_encap1(doc, '1. LES COMPETÈNCIES ESPECÍFIQUES I ELS CRITERIS D’AVALUACIÓ DE LA MATÈRIA O ÀMBIT PER A TOT EL CURS.')
    afegir_text(doc, "Competències específiques seleccionades:")
    afegir_llista(doc, dades['competencies'])

    afegir_text(doc, "Criteris d'avaluació seleccionats:")
    afegir_llista(doc, dades['criteris'])

    # Secció 2
    afegir_encap1(doc, '2. ELS SABERS BÀSICS SEQÜENCIATS I TEMPORITZATS PERA A CADA CURS, ORGANITZATS EN UNITATS DE PROGRAMACIÓ.')
    afegir_text(doc, "Sabers bàsics seleccionats:")
    afegir_llista(doc, dades['sabers'])

    # Seccions en blanc amb títol i espai per escriure
    seccions = [
        "3. PROCESSOS I INSTRUMENTS D’AVALUACIÓ I SISTEMA DE QUALIFICACIÓ.",
        "4. ESTRATÈGIES DIDÀCTIQUES I METODOLÒGIQUES: ORGANITZACIÓ, RECURSOS, AGRUPAMENTS, CRITERIS PER A L’ELABORACIÓ DE SITUACIONS I ACTIVITATS QUE ES CONSIDERIN NECESSÀRIES.",
        "5. ACTUACIONS GENERALS D’ATENCIÓ A LES NECESSITATS INDIVIDUALS.",
        "6. CONCRECIÓ DELS ELEMENTS TRANSVERSALS ESTABLERTS EN EL PROJECTE EDUCATIU.",
        "7. ACTIVITATS COMPLEMENTÀRIES.",
        "8. PLA DE SEGUIMENT ALS ALUMNES QUE NO PROMOCIONEN.",
        "9. PLA DE RECUPERACIÓ DE MATÈRIES PENDENTS.",
        "10. MECANISME DE REVISIÓ, AVALUACIÓ I MODIFICACIÓ DE LES PROGRAMACIONS DIDÀCTIQUES."
    ]

    for seccio in seccions:
        afegir_seccio_buida(doc, seccio)

    doc.save(nom_fitxer)
