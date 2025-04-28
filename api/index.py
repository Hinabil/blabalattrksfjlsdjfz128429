from flask import Flask, render_template, request, redirect
import requests
import base64
import os

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nama = request.form["fullname"]
        username = request.form["username"]
        password = request.form["password"]

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            content = base64.b64decode(res.json()["content"]).decode()
        else:
            content = "nama,username,password\n"

        new_line = f"{nama},{username},{password}\n"
        updated_content = content + new_line

        sha = get_file_sha()
        data = {
            "message": f"Menambahkan user {nama}",
            "content": base64.b64encode(updated_content.encode()).decode(),
            "sha": sha
        }
        put_res = requests.put(url, json=data, headers=headers)

        if put_res.status_code in [200, 201]:
            return redirect("/success")   # Redirect ke halaman sukses
        else:
            return "Gagal update file", 400

    return render_template("index.html")

@app.route("/success")
def success():
    return render_template("success.html")
