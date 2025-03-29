from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

# **1️⃣ Konfigurasi Akun**
USERNAME = "wisnuandrean13@gmail.com"
PASSWORD = "musrenbangdki"

# **2️⃣ Setup WebDriver**
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# **1️⃣ Akses Halaman Login**
login_url = "https://akun.jakarta.go.id/login"
driver.get(login_url)
time.sleep(3)

# **2️⃣ Masukkan Username & Password**
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
driver.find_element(By.NAME, "password").send_keys(PASSWORD)

# **3️⃣ Klik Tombol Login**
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button/span[contains(text(), 'Masuk')]"))
)
login_button.click()

# **4️⃣ Tunggu Hingga Login Berhasil**
WebDriverWait(driver, 10).until(EC.url_contains("akun.jakarta.go.id"))
print("✅ Login Berhasil!")

# **5️⃣ Navigasi ke Halaman Usulan**
url_usulan = "https://musrenbang.jakarta.go.id/usulan_langsung/home"
driver.get(url_usulan)
time.sleep(3)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "v-card")))
print("✅ Berhasil mengakses halaman usulan!")
start_time = time.time()
# **6️⃣ Scraping Data Usulan & Detail**
count = 0

with open("data_usulan_detail.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["No", "Kode Tracking", "Permasalahan", "Usulan Kegiatan", "Volume / Satuan", "Tipe Usulan", 
                     "Kabupaten / Kota", "Kecamatan", "Kelurahan", "RW", "RT", 
                     "Keterangan", "Nama Pengusul", "Alamat", "Nomor Telepon", "Email", 
                     "Status Verifikasi", "PD/UKPD Sebelum", "PD/UKPD Setelah", "Jenis Usulan", "Catatan Penyelia"])  # **Hapus Titik Lokasi & Foto Bukti**

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("div", class_="v-card")

        for index, card in enumerate(cards):
            # **Klik Tombol Detail**
            if count == 0 or count % 10 != 0:
                try:
                    detail_button_xpath = f"(//button[contains(@class, 'mdi-view-headline')])[{index+1}]"
                    detail_button_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, detail_button_xpath))
                    )
                    detail_button_element.click()
                    time.sleep(2)  # Tunggu modal terbuka
    
                    # **Pastikan Modal Terbuka**
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'v-card__text')]"))
                    )
    
                    # **Ambil Data Detail dari Modal**
                    detail_soup = BeautifulSoup(driver.page_source, "html.parser")
    
                    def get_detail(label):
                        """
                        Cari elemen berdasarkan label `v-subheader`, lalu ambil value di div berikutnya (`v-card__text`).
                        """
                        try:
                            label_element = detail_soup.find("div", class_="v-subheader", string=label)
                            if label_element:
                                value_element = label_element.find_parent("div").find_next_sibling("div")
                                return value_element.find("div", class_="v-card__text").text.strip() if value_element else "Tidak Ada Data"
                            return "Tidak Ada Data"
                        except:
                            return "Tidak Ada Data"
    
                    kode_tracking = get_detail("Kode Tracking")
                    permasalahan = get_detail("Permasalahan")
                    usulan_kegiatan = get_detail("Usulan Kegiatan")
                    volume_satuan = get_detail("Volume / Satuan")
                    tipe_usulan = get_detail("Tipe Usulan")
                    kabupaten = get_detail("Kabupaten / Kota")
                    kecamatan = get_detail("Kecamatan")
                    kelurahan = get_detail("Kelurahan")
                    rw = get_detail("RW")
                    rt = get_detail("RT")
                    keterangan = get_detail("Keterangan")
    
                    # **Ambil Biodata Pengusul**
                    nama_pengusul = get_detail("Nama Lengkap")
                    alamat = get_detail("Alamat")
                    nomor_telepon = get_detail("Nomor Telepon")
                    email = get_detail("E-Mail")
    
                    # **Ambil Status Verifikasi & PD/UKPD**
                    status_verifikasi = get_detail("Status")
                    pd_ukpd_sebelum = get_detail("PD/UKPD Sebelum")
                    pd_ukpd_setelah = get_detail("PD/UKPD Setelah")
                    jenis_usulan = get_detail("Jenis Usulan")
                    catatan_penyelia = get_detail("Catatan Penyelia")
    
                    # **Tutup Modal Detail**
                    close_button_xpath = "//button[contains(@class, 'v-btn--icon')]"
                    close_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, close_button_xpath))
                    )
                    close_button.click()
                    time.sleep(2)
    
                    # **Kembali ke Halaman Usulan**
                    driver.back()
                    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "v-card")))
                    time.sleep(3)
            
                    print(count)
                except Exception as e:
                    print(f"⚠️ ERROR: {e}")
                    kode_tracking = permasalahan = usulan_kegiatan = volume_satuan = tipe_usulan = kabupaten = kecamatan = kelurahan = rw = rt = keterangan = nama_pengusul = alamat = nomor_telepon = email = status_verifikasi = pd_ukpd_sebelum = pd_ukpd_setelah = jenis_usulan = catatan_penyelia = "Gagal Mengambil Detail"
                
                count += 1
                print(f"[{count}] Kode: {kode_tracking} | Status: {status_verifikasi} | PD: {pd_ukpd_sebelum} → {pd_ukpd_setelah}")
                print("Total waktu: ", time.time()-start_time)
                writer.writerow([count, kode_tracking, permasalahan, usulan_kegiatan, volume_satuan, tipe_usulan, 
                                 kabupaten, kecamatan, kelurahan, rw, rt, 
                                 keterangan, nama_pengusul, alamat, nomor_telepon, email, 
                                 status_verifikasi, pd_ukpd_sebelum, pd_ukpd_setelah, jenis_usulan, catatan_penyelia])

            else:
                try:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Halaman selanjutnya']"))
                    )
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)
                    count +=1
                except:
                    print(f"✅ Scraping selesai! Total data yang diambil: {count}")
                    break
            
        # **7️⃣ Klik Tombol "Next" Jika Ada**
        

# **8️⃣ Tutup WebDriver**
driver.quit()
print("✅ Semua data disimpan di 'data_usulan_detail.csv'.")
