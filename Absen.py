from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='NIP/NPM']").send_keys(username)  # Ganti ID sesuai elemen di situs
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='Password']").send_keys(password)  # Ganti ID sesuai elemen di situs
        driver.find_element(By.XPATH, "//button[text()='Login']").click()  # Ganti ID sesuai elemen di situs
        time.sleep(3)
        print(f"Berhasil login untuk username: {nama}")

        # Buka halaman absen
        driver.get(url_absen)
        time.sleep(5)

        # Klik tombol absen
        driver.find_element(By.XPATH, "//button[text()='Konfirmasi Kehadiran']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//button[text()='Konfirmasi']").click()
        time.sleep(3)

        print(f"Absen berhasil untuk : {nama}")
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
