from flask import Flask, render_template, request, g, redirect, url_for, session
from psycopg2 import pool
import os

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')

app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# 🔁 Inisialisasi connection pool saat pertama kali app dijalankan
db_pool = pool.SimpleConnectionPool(
    1, 10,  # min & max koneksi aktif
    host=os.environ.get("PGHOST"),
    database=os.environ.get("PGDATABASE"),
    user=os.environ.get("PGUSER"),
    password=os.environ.get("PGPASSWORD")
)

# 🔄 Ambil koneksi dari pool setiap request
@app.before_request
def get_db_conn():
    g.db_conn = db_pool.getconn()
    g.cursor = g.db_conn.cursor()

# 🧹 Kembalikan koneksi ke pool setelah request selesai
@app.teardown_request
def close_db_conn(exception=None):
    if hasattr(g, 'cursor'):
        g.cursor.close()
    if hasattr(g, 'db_conn'):
        db_pool.putconn(g.db_conn)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/tambah_proses", methods=["POST"])
def tambah():
    nama = request.form.get("fullname")
    username = request.form.get("username")
    password = request.form.get("password")

    try:
        g.cursor.execute("""
            INSERT INTO "data absen" (nama, username, password)
            VALUES (%s, %s, %s)
        """, (nama, username, password))
        g.db_conn.commit()
        return render_template("success.j2", username=nama)
    except Exception as e:
        g.db_conn.rollback()
        return f"Gagal menyimpan ke database: {e}", 500


@app.route("/login_admin")
def login_admin():
    return app.send_static_file("login_admin.html")


@app.route("/proses_login", methods=["POST"])
def proses_login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        g.cursor.execute("""
            SELECT * FROM "data absen"
            WHERE id = 1 AND username = %s AND password = %s
        """, (username, password))
        user = g.cursor.fetchone()

        if user:
                  session['admin'] = user[1]
                  return redirect(url_for("dashboard"))
        else:
                  return "Login gagal. Username atau password salah.", 401
    except Exception as e:
        return f"Terjadi error: {e}", 500


@app.route("/dashboard")
def dashboard():
   try:
     if "admin" not in session:
         return redirect(url_for("login_admin"))

     g.cursor.execute('SELECT id, nama, username, password FROM "data absen"')
     semua_user = g.cursor.fetchall()
     return render_template("dashboard_admin.j2", nama=session['admin'], data=semua_user)
   except Exception as e:
      return f"Terjadi error: {e}", 500
               

if __name__ == "__main__":
    app.run(debug=True)
