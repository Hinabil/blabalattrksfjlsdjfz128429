from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys 
import time

# Konfigurasi
username = "2404111010055"  # Ganti dengan username Anda
password = "15927386"  # Ganti dengan password Anda
url_login = "https://simkuliah.usk.ac.id/"  # URL halaman login
url_absen = "https://simkuliah.usk.ac.id/index.php/absensi"  # URL halaman absen


service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service)

def otomatis_absen():
    
    try:
        # Buka halaman login
        driver.get(url_login)
        time.sleep(2)
        
        # Masukkan username dan password
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='NIP/NPM']").send_keys(username)  # Ganti ID sesuai elemen di situs
        driver.find_element(By.XPATH, "//input[@class='form-control' and @placeholder='Password']").send_keys(password)  # Ganti ID sesuai elemen di situs
        driver.find_element(By.XPATH, "//button[text()='Login']").click()  # Ganti ID sesuai elemen di situs
        time.sleep(3)
        print("berhasil masuk")
        
        # Buka halaman absen
        driver.get(url_absen)
        time.sleep(5)
        
        # Klik tombol absen
        driver.find_element(By.XPATH, "//button[text()='Konfirmasi Kehadiran']").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//button[text()='Konfirmasi']").click() 
        time.sleep(3)
        
        print("Absen berhasil!")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        driver.quit()

# Jalankan fungsi
otomatis_absen()
