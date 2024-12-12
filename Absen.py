from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

# Konfigurasi
url_login = "https://simkuliah.usk.ac.id/"  # URL halaman login
url_absen = "https://simkuliah.usk.ac.id/index.php/absensi"  # URL halaman absen

chrome_service = Service("/usr/local/bin/chromedriver")

# Opsi Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Menjalankan tanpa GUI (opsional untuk server)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Inisialisasi WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def otomatis_absen(nama, username, password):
    try:
        # Buka halaman login
        driver.get(url_login)
        time.sleep(2)

        # Masukkan username dan password
        driver.get(url_login)

        # Tunggu elemen login tersedia
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control' and @placeholder='NIP/NPM']"))
        ).send_keys(username)
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control' and @placeholder='Password']"))
        ).send_keys(password)
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        ).click()
        print(f"Berhasil login untuk : {nama}")

        # Buka halaman absen
        driver.get(url_absen)
        # Klik tombol absen
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Konfirmasi Kehadiran']"))
        ).click()
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Konfirmasi']"))
        ).click()

        print(f"Absen berhasil untuk : {nama}")
    except TimeoutException:
        print(f"Belum ada absen untuk {nama}, absen gagal.")
    except Exception as e:
        print(f"Terjadi kesalahan untuk {nama}: {e}")

# Membaca file CSV dan menjalankan otomatis absen untuk setiap user
try:
    with open("user.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            nama = row["nama"]
            username = row["username"]
            password = row["password"]
            
            otomatis_absen(nama, username, password)
finally:
    driver.quit()
    print("Proses selesai.")
