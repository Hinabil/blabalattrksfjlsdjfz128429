from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import csv

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

driver.set_window_size(1920, 1080)

def take_screenshot(step, nama):
    """Fungsi untuk mengambil screenshot dan menyimpannya dengan nama yang sesuai."""
    screenshot_name = f"screenshot_{nama}_{step}.png"
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot diambil: {screenshot_name}")
    
def login(nama, username, password):
    try:
        # Buka halaman login
        driver.get(url_login)
        
        take_screenshot("login_page", nama)

        # Tunggu elemen login tersedia dan masukkan username serta password
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control' and @placeholder='NIP/NPM']"))
        ).send_keys(username)
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@class='form-control' and @placeholder='Password']"))
        ).send_keys(password)
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
        ).click()
        
        take_screenshot("login_berhasil", nama)
        print(f"Login berhasil untuk: {nama}")
        return True
    except TimeoutException:
        take_screenshot("login_gagal", nama)
        print(f"Login tidak berhasil untuk: {nama}")
        return False
    except Exception as e:
        take_screenshot("login_error", nama)
        print(f"Terjadi kesalahan saat login untuk {nama}: {e}")
        return False

def absen(nama):
    try:
        # Buka halaman absen
        driver.get(url_absen)

        # Tunggu dan klik tombol "Konfirmasi Kehadiran"
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Konfirmasi Kehadiran']"))
        ).click()
        take_screenshot("konfirmasi_kehadiran", nama)

        # Tunggu dan klik tombol "Konfirmasi"
        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Konfirmasi']"))
        ).click()
        take_screenshot("konfirmasi_berhasil", nama)

        WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='OK']"))
        ).click()
        take_screenshot("absen_ok", nama)

        print(f"Absen berhasil untuk: {nama}")
        driver.get(url_logout)
    except TimeoutException:
        take_screenshot("absen_belum_ada", nama)
        print(f"Absen belum ada untuk: {nama}")
        driver.get(url_logout)
    except Exception as e:
        take_screenshot("absen_error", nama)
        print(f"Terjadi kesalahan saat absen untuk {nama}: {e}")
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
