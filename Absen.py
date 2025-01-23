from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

# Konfigurasi
url_login = "https://simkuliah.usk.ac.id/index.php/login"  # URL halaman login
url_absen = "https://simkuliah.usk.ac.id/index.php/absensi"  # URL halaman absen
url_logout = "https://simkuliah.usk.ac.id/index.php/login/logout"

chrome_service = Service("/usr/local/bin/chromedriver")

# Opsi Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan tanpa GUI (opsional untuk server)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inisialisasi WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

#setel ukuran layar hd
driver.set_window_size(1920, 1080)
                       
# Direktori untuk menyimpan screenshot
os.makedirs("screenshots", exist_ok=True)

def take_screenshot(step, nama):
    """Ambil screenshot dan simpan dengan nama file sesuai proses."""
    filename = f"screenshots/{nama}_{step}.png"
    driver.save_screenshot(filename)
    print(f"Tangkapan layar diambil: {filename}")

def login(nama, username, password):
    try:
        # Buka halaman login
        driver.get(url_login)
        take_screenshot("login_page", nama)

        # Masukkan username dan password
        time.sleep(2)  # Tunggu halaman memuat
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='NIP/NPM']").send_keys(username)
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='Password']").send_keys(password)

        # Klik tombol login
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        time.sleep(2)  # Tunggu proses login selesai
        take_screenshot("login_success", nama)
        print(f"Login berhasil untuk: {nama}")
        return True
    except Exception as e:
        take_screenshot("login_error", nama)
        print(f"Login tidak berhasil untuk {nama}: {e}")
        return False

def absen(nama):
    try:
        # Buka halaman absen
        driver.get(url_absen)
        time.sleep(1)
        take_screenshot("absen_page", nama)
        time.sleep(1)  # Tunggu halaman memuat

        # Klik tombol "Konfirmasi Kehadiran"
        driver.find_element(By.XPATH, "//button[text()='Konfirmasi Kehadiran']").click()
        time.sleep(1)  # Tunggu tombol "Konfirmasi Kehadiran" diproses
        take_screenshot("absen_confirm_button", nama)

        # Klik tombol "Konfirmasi"
        driver.find_element(By.XPATH, "//button[text()='Konfirmasi']").click()
        time.sleep(2)  # Tunggu konfirmasi selesai
        take_screenshot("absen_success", nama)

        print(f"Absen berhasil untuk: {nama}")
        driver.get(url_logout)
        take_screenshot("logout", nama)
    except Exception as e:
        take_screenshot("absen_belum ada/error", nama)
        print(f"Belum ada absen untuk {nama}")
        driver.get(url_logout)

# Membaca file CSV dan menjalankan otomatis absen untuk setiap user
try:
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nama = row["nama"]
            username = row["username"]
            password = row["password"]

            # Proses login
            if login(nama, username, password):
                # Jika login berhasil, lanjutkan ke absen
                absen(nama)
finally:
    driver.quit()
    print("Proses selesai.")
