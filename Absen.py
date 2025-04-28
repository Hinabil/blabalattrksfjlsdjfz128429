from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import psycopg2
import os
from dotenv import load_dotenv
# Konfigurasi
url_login = "https://simkuliah.usk.ac.id/index.php/login"
url_absen = "https://simkuliah.usk.ac.id/index.php/absensi"
url_logout = "https://simkuliah.usk.ac.id/index.php/login/logout"

chrome_service = Service("/usr/local/bin/chromedriver")

# Opsi Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tanpa GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inisialisasi WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# Setel ukuran layar HD
driver.set_window_size(1920, 1080)

# Direktori untuk screenshot
os.makedirs("screenshots", exist_ok=True)

# Koneksi ke NeonDB

def get_db_connection():
    conn = psycopg2.connect(
        dbname=os.environ["NEON_DB"],
        user=os.environ["NEON_USER"],
        password=os.environ["NEON_PASSWORD"],
        host=os.environ["NEON_HOST"],
        sslmode="require"
    )
    return conn

def take_screenshot(step, nama):
    filename = f"screenshots/{nama}_{step}.png"
    driver.save_screenshot(filename)
    print(f"Tangkapan layar diambil: {filename}")

def login(nama, username, password):
    try:
        driver.get(url_login)
        take_screenshot("login_page", nama)

        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='NIP/NPM']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='Password']").send_keys(password)

        time.sleep(1)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        time.sleep(2)
        take_screenshot("login_success", nama)
        print(f"Login berhasil untuk: {nama}")
        return True
    except Exception as e:
        take_screenshot("login_error", nama)
        print(f"Login gagal untuk {nama}: {e}")
        return False

def absen(nama):
    try:
        driver.get(url_absen)
        time.sleep(1)
        take_screenshot("absen_page", nama)
        time.sleep(1)

        driver.find_element(By.XPATH, "//button[text()='Konfirmasi Kehadiran']").click()
        time.sleep(1)
        take_screenshot("absen_confirm_button", nama)

        driver.find_element(By.XPATH, "//button[text()='Konfirmasi']").click()
        time.sleep(2)
        take_screenshot("absen_success", nama)

        print(f"Absen berhasil untuk: {nama}")
        driver.get(url_logout)
        take_screenshot("logout", nama)
    except Exception as e:
        take_screenshot("absen_error", nama)
        print(f"Gagal absen untuk {nama}: {e}")
        driver.get(url_logout)

def get_users_from_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT nama, username, password FROM "data absen"')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return users

# Main logic
try:
    users = get_users_from_db()
    for nama, username, password in users:
        if login(nama, username, password):
            absen(nama)
finally:
    driver.quit()
    print("Proses selesai.")
