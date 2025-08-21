from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import psycopg2
import os

# 🔁 Muat variabel lingkungan

# 🔧 URL Konstanta
URL_LOGIN = "https://simkuliah.usk.ac.id/index.php/login"
URL_ABSEN = "https://simkuliah.usk.ac.id/index.php/absensi"
URL_LOGOUT = "https://simkuliah.usk.ac.id/index.php/login/logout"

# 🛠️ Setup ChromeDriver
chrome_service = Service("/usr/local/bin/chromedriver")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 🖼️ Direktori tangkapan layar
os.makedirs("screenshots", exist_ok=True)

def take_screenshot(driver, step, nama):
    filename = f"screenshots/{nama}_{step}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot: {filename}")

def login(driver, nama, username, password):
    try:
        driver.get(URL_LOGIN)
        time.sleep(2)
        take_screenshot(driver, "login_page", nama)

        driver.find_element(By.XPATH, "//input[@placeholder='NIP/NPM']").send_keys(username)
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys(password)
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        time.sleep(2)
        take_screenshot(driver, "login_success", nama)
        print(f"✅ Login berhasil: {nama}")
        return True
    except Exception as e:
        take_screenshot(driver, "login_error", nama)
        print(f"❌ Login gagal: {nama} - {e}")
        return False

def absen(driver, nama):
    try:
        driver.get(URL_ABSEN)
        time.sleep(1)
        take_screenshot(driver, "absen_page", nama)

        driver.find_element(By.XPATH, "//button[text()='Konfirmasi Kehadiran']").click()
        time.sleep(1)
        take_screenshot(driver, "absen_confirm_button", nama)

        driver.find_element(By.XPATH, "//button[text()='Konfirmasi']")[1].click()
        time.sleep(2)
        take_screenshot(driver, "absen_success", nama)

        print(f"🟢 Absen sukses: {nama}")
    except Exception as e:
        take_screenshot(driver, "absen_error", nama)
        print(f"🔴 Gagal absen: {nama} - {e}")
    finally:
        driver.get(URL_LOGOUT)
        take_screenshot(driver, "logout", nama)

def get_users_from_db():
    # 🔒 Hanya koneksi saat diperlukan
    try:
        with psycopg2.connect(
            user=os.environ["PGUSER"],
            password=os.environ["PGPASSWORD"],
            host=os.environ["PGHOST"],
            database=os.environ["PGDATABASE"],
            sslmode="require"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT nama, username, password FROM "data absen"')
                return cur.fetchall()
    except Exception as e:
        print(f"⚠️ Gagal koneksi ke database: {e}")
        return []

def main():
    users = get_users_from_db()
    if not users:
        print("⚠️ Tidak ada data user ditemukan.")
        return

    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.set_window_size(1920, 1080)

    try:
        for nama, username, password in users:
            if login(driver, nama, username, password):
                absen(driver, nama)
    finally:
        driver.quit()
        print("✅ Proses selesai dan browser ditutup.")

if __name__ == "__main__":
    main()
