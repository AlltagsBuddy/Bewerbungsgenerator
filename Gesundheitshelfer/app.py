from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from io import BytesIO
from docx import Document
from fpdf import FPDF

import os

openai_key = os.getenv("OPENAI_API_KEY")
google_key = os.getenv("GOOGLE_API_KEY")



app = Flask(__name__, template_folder='templates')
CORS(app)

@app.route('/')
def serve_html():
    return render_template('gesundheit.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()

    diagnose = "Verdachtsdiagnose: Reizdarm"
    behandlung = "- Iberogast oder Buscopan (rezeptfrei)\n- Kamillentee, Wärme, Stressreduktion"
    ernaehrung = "- Ballaststoffarme Ernährung\n- Kleine Mahlzeiten\n- Wenig Kaffee"
    arzt = "Hausarzt oder Gastroenterologe"
    hinweis = "Diese Einschätzung ersetzt keinen Arztbesuch. Bei Unsicherheit bitte medizinische Hilfe in Anspruch nehmen."

    text = f"""
🔍 {diagnose}

Empfohlene Behandlung:
{behandlung}

Ernährung & Verhalten:
{ernaehrung}

Fachärztliche Empfehlung:
{arzt}

⚠️ Hinweis:
{hinweis}
"""
    return jsonify({"brieftext": text})

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    data = request.get_json()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in data.get("brieftext", "").split("\n"):
        pdf.multi_cell(0, 10, line)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="gesundheitshelfer.pdf", mimetype='application/pdf')

@app.route('/api/export/docx', methods=['POST'])
def export_docx():
    data = request.get_json()
    doc = Document()
    for line in data.get("brieftext", "").split("\n"):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="gesundheitshelfer.docx", mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
