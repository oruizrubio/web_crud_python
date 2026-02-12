import os
import requests
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Configuración
# Configuración usando Variables de Entorno
# El segundo parámetro es un valor por defecto (opcional)
URL_BASE = os.environ.get("SUPABASE_URL", "https://sreimemtayqwyyhiihcz.supabase.co/rest/v1/productos")
KEY = os.environ.get("SUPABASE_KEY")
HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

@app.route('/')
def index():
    # El parámetro verify=False ignora el error de certificado
    response = requests.get(URL_BASE, headers=HEADERS, params={"select": "*"}, verify=False)
    return render_template('index.html', productos=response.json())

@app.route('/agregar', methods=['POST'])
def agregar():
    datos = {
        "codigo": request.form.get('codigo'),
        "descripcion": request.form.get('descripcion')
    }
    requests.post(URL_BASE, headers=HEADERS, json=datos, verify=False)
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    requests.delete(f"{URL_BASE}?codigo=eq.{id}", headers=HEADERS, verify=False)
    return redirect(url_for('index'))

@app.route('/editar/<id>', methods=['POST'])
def editar(id):
    datos = {"descripcion": request.form.get('descripcion')}
    requests.patch(f"{URL_BASE}?codigo=eq.{id}", headers=HEADERS, json=datos, verify=False)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
