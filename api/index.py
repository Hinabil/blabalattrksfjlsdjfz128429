from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

# Koneksi ke NeonDB
conn = psycopg2.connect(
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        host=os.environ["PGHOST"],
        sslmode="require"
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

@app.route("/login_admin")
def login_admin():
    return app.send_static_file("login_admin.html")

@app.route("/proses_login", methods=["POST"])
def proses_login():
    if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    cursor.execute("""
        SELECT * FROM data_absen
        WHERE id = 1 AND username = %s AND password = %s
    """, (username, password))
    user = cursor.fetchone()

    if user:
        return render_template("dashboard_admin.j2", nama=user[1])
    else:
        return "Login gagal. Username atau password salah.", 401

if __name__ == "__main__":
    app.run(debug=True)
