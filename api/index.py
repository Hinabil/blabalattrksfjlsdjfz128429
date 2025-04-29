from flask import Flask, render_template, request, redirect
import requests
import psycopg2
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
# Koneksi ke NeonDB
conn = psycopg2.connect(
    host=os.environ.get("PGHOST"),
    dbname=os.environ.get("PGDATABASE"),
    user=os.environ.get("PGUSER"),
    password=os.environ.get("PGPASSWORD")
)
cursor = conn.cursor()

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

if __name__ == "__main__":
    app.run(debug=True)

