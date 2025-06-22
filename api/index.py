from flask import Flask, render_template, request, g, redirect, url_for, session
from psycopg2 import pool
from flask import send_from_directory
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

def check_for_maintenance():
    if True:
        return render_template('maintenance.html'), 503

# 🧹 Kembalikan koneksi ke pool setelah request selesai
@app.teardown_request
def close_db_conn(exception=None):
    if hasattr(g, 'cursor'):
        g.cursor.close()
    if hasattr(g, 'db_conn'):
        db_pool.putconn(g.db_conn)

@app.route('/ads.txt')
def ads():
    return send_from_directory('static', 'ads.txt')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@app.route('/sitemap.xml')
def sitemap_xml():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')
            
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
            
@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/donasi")
def donasi():
    return app.send_static_file("donasi.html")

@app.route("/tambah_proses", methods=["POST"])
def tambah():
    nama = request.form.get("fullname")
    username = request.form.get("username")
    password = request.form.get("password")
    jurusan = request.form.get("jurusan")

    try:
        g.cursor.execute("""
            INSERT INTO "data absen" (nama, username, password, jurusan)
            VALUES (%s, %s, %s, %s)
        """, (nama, username, password, jurusan))
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
                
@app.route("/proses_logout", methods=["POST"])
def proses_logout():
    try:
         session.clear()  
         return redirect(url_for("login_admin")) 
    except Exception as e:
        return f"Terjadi error: {e}", 500

@app.route("/dashboard")
def dashboard():
    try:
        if "admin" not in session:
            return redirect(url_for("login_admin"))

        # Ambil semua user dengan kolom yang sesuai template
        g.cursor.execute('SELECT id, nama, jurusan, username, password FROM "data absen"')
        rows = g.cursor.fetchall()

        # Mapping hasil ke dalam format dictionary sesuai dengan template
        users = []
        for row in rows:
            users.append({
                'id': row[0],
                'full_name': row[1],       # nama → full_name
                'department': row[2],      # bagian → department
                'username': row[3],
                'password': row[4],
            })

        current_user = {
            'username': session['admin'],
            'role': 'Super Admin'  # Atau ambil dari DB kalau ingin dinamis
        }

        return render_template("Dashboard_admin.j2", nama=session['admin'], users=users, current_user=current_user)
    except Exception as e:
        return f"Terjadi error: {e}", 500

               

if __name__ == "__main__":
    app.run(debug=True)
