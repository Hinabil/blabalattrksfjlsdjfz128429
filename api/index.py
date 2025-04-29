from flask import Flask, render_template, request, redirect
import requests
import base64
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")
FILE_PATH = "user.csv"

def get_file_sha():
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/tambah_proses", methods=["POST"])
def tambah():
    if request.method == "POST":
        nama = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            cursor.execute("""
                INSERT INTO data_absen (nama, username, password)
                VALUES (%s, %s, %s)
            """, (nama, username, password))
            conn.commit()
            return render_template("success.j2", username=nama)
        except Exception as e:
            conn.rollback()
            return f"Gagal menyimpan ke database: {e}", 500
