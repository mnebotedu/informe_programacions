
from docx import Document

def generar_docx(dades, nom_fitxer='informe.docx'):
    doc = Document()
    doc.add_heading('Informe de programació', 0)

    doc.add_paragraph(f"Nivell educatiu: {dades['nivell']}")
    doc.add_paragraph(f"Curs: {dades['curs']}")
    doc.add_paragraph(f"Matèria: {dades['materia']}")

    doc.add_paragraph("Competències específiques seleccionades:")
    for ce in dades['competencies']:
        doc.add_paragraph(f" {ce}", style='List Bullet')

    doc.add_paragraph("Criteris d'avaluació seleccionats:")
    for cr in dades['criteris']:
        doc.add_paragraph(f" {cr}", style='List Bullet')

    doc.add_paragraph("Sabers bàsics seleccionats:")
    for sb in dades['sabers']:
        doc.add_paragraph(f" {sb}", style='List Bullet')

    doc.save(nom_fitxer)
