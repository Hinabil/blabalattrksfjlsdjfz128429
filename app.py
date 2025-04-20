import os
import csv
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Template HTML sederhana
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Tambah Data Absen</title>
</head>
<body>
    <h1>Form Tambah User Absen</h1>
    <form method="POST">
        <label>Nama:</label><br>
        <input type="text" name="nama" required><br><br>
        <label>Username:</label><br>
        <input type="text" name="username" required><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" required><br><br>
        <button type="submit">Tambah</button>
    </form>

    <h2>Daftar User:</h2>
    <ul>
        {% for user in users %}
            <li>{{ user['nama'] }} - {{ user['username'] }}</li>
        {% endfor %}
    </ul>
</body>
</html>
'''

CSV_FILE = 'user.csv'

# Pastikan file user.csv sudah ada
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['nama', 'username', 'password'])
        writer.writeheader()

def read_users():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def add_user(nama, username, password):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['nama', 'username', 'password'])
        writer.writerow({'nama': nama, 'username': username, 'password': password})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form['nama']
        username = request.form['username']
        password = request.form['password']
        add_user(nama, username, password)
        return redirect(url_for('index'))
    
    users = read_users()
    return render_template_string(HTML_TEMPLATE, users=users)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
