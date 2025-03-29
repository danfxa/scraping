from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time
import argparse

# Argument Parser
parser = argparse.ArgumentParser(description="Scrape data musrenbang berdasarkan ID range")
parser.add_argument("a", type=int, help="Part")
parser.add_argument("initial",type = int, help = "Nilai awal")
parser.add_argument("step",type = int, help = "Step")
parser.add_argument("end",type = int, help = "akhir")
args = parser.parse_args()

# **Konfigurasi Akun**
USERNAME = "golkar.dadiyono"
PASSWORD = "dkijakartakosong123"

# **Setup WebDriver**
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# **Akses Halaman Login**
login_url = "https://akun.jakarta.go.id/login"
driver.get(login_url)
time.sleep(3)

# **Masukkan Username & Password**
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)

# **Klik Tombol Login**
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button/span[contains(text(), 'Masuk')]"))
)
login_button.click()

# **Tunggu Hingga Login Berhasil**
WebDriverWait(driver, 10).until(EC.url_contains("akun.jakarta.go.id"))
print("✅ Login Berhasil!")

path = "/Users/dprddkijakarta/Documents/scraping/scraping/data/reses"
# **Buka File CSV**

step = args.step
a = args.a
init_page = args.initial
end_page = args.end
s_time = time.time()

with open(path+"/data_reses_detail_p"+str(a)+".csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "No", "Nama Fraksi", "Isi Reses", "Jenis Reses", "Kelompok Isu", "Standardisasi Kegiatan", "Jenis Usulan",
        "Keyword", "Nama Pengusul", "No HP", "Alamat Pengusul", "Kelurahan Pengusul", "Kecamatan Pengusul",
        "Kab/Kota Pengusul", "RW Pengusul", "RT Pengusul", "Alamat Usulan", "Kelurahan Usulan", "Kecamatan Usulan",
        "Kab/Kota Usulan", "RW Usulan", "RT Usulan", "PD/UKPD Tujuan", "Diperbaharui oleh", "Diperbaharui pada"
    ])
    
    count = 0

    for i in range(init_page, end_page):
        url = f"https://musrenbang-reses.bapedadki.net/reses/{i}/home?t=1"
        driver.get(url)
        time.sleep(1)

        # **Ambil Data Detail**
        soup = BeautifulSoup(driver.page_source, "html.parser")

        def get_detail(label):
            try:
                element = soup.find("div", class_="v-subheader", string=label)
                if element:
                    return element.find_parent("div").find_next_sibling("div").text.strip()
                return "Tidak Ada Data"
            except:
                return "Tidak Ada Data"

        nama_fraksi = get_detail("Nama Fraksi")
        isi_reses = get_detail("Isi Reses")
        jenis_reses = get_detail("Jenis Reses")
        kelompok_isu = get_detail("Kelompok Isu")
        standardisasi_kegiatan = get_detail("Standardisasi Kegiatan")
        jenis_usulan = get_detail("Jenis Usulan")
        keyword = get_detail("Keyword")
        nama_pengusul = get_detail("Nama Pengusul (Warga)")
        no_hp = get_detail("No HP Pengusul")
        alamat_pengusul = get_detail("Alamat Pengusul")
        kelurahan_pengusul = get_detail("Kelurahan Pengusul")
        kecamatan_pengusul = get_detail("Kecamatan Pengusul")
        kab_kota_pengusul = get_detail("Kab/Kota Pengusul")
        rw_pengusul = get_detail("RW Pengusul")
        rt_pengusul = get_detail("RT Pengusul")
        alamat_usulan = get_detail("Alamat Usulan")
        kelurahan_usulan = get_detail("Kelurahan Usulan")
        kecamatan_usulan = get_detail("Kecamatan Usulan")
        kab_kota_usulan = get_detail("Kab/Kota Usulan")
        rw_usulan = get_detail("RW Usulan")
        rt_usulan = get_detail("RT Usulan")
        pd_ukpd_tujuan = get_detail("PD/UKPD Tujuan")
        diperbaharui_oleh = get_detail("Diperbaharui oleh")
        diperbaharui_pada = get_detail("Diperbaharui pada")

        count += 1
        est = ((time.time()-s_time)/count*(end_page-(init_page+count)))/60
        print(f"estimasi selesai: {est}")
        print(f"[{count}] Nama Fraksi: {nama_fraksi} | Jenis Usulan: {jenis_usulan} | PD/UKPD: {pd_ukpd_tujuan}")
        
        if not nama_fraksi:
            continue
        
        writer.writerow([
            count, nama_fraksi, isi_reses, jenis_reses, kelompok_isu, standardisasi_kegiatan, jenis_usulan,
            keyword, nama_pengusul, no_hp, alamat_pengusul, kelurahan_pengusul, kecamatan_pengusul,
            kab_kota_pengusul, rw_pengusul, rt_pengusul, alamat_usulan, kelurahan_usulan, kecamatan_usulan,
            kab_kota_usulan, rw_usulan, rt_usulan, pd_ukpd_tujuan, diperbaharui_oleh, diperbaharui_pada
        ])

# **Tutup WebDriver**
driver.quit()
print("✅ Semua data disimpan di 'data_reses_detail.csv'.")
