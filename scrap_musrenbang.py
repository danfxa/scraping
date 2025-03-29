#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  4 01:41:21 2025

@author: dprddkijakarta
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import time

# Setup Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# **5️⃣ Navigasi ke Halaman Usulan**
url_usulan = "https://musrenbang.jakarta.go.id/public_musrenbang/home?tahun=2022"
driver.get(url_usulan)
time.sleep(3)

# **6️⃣ Pastikan Tabel Termuat**
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
print("✅ Berhasil mengakses halaman usulan!")

path = "/Users/dprddkijakarta/Documents/scraping/scraping/data/musrenbang"

# **1️⃣ Ubah jumlah data per halaman menjadi 100**
try:
    # Klik dropdown "Baris per halaman"
    dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".v-select__selections"))
    )
    dropdown.click()
    time.sleep(2)  # Tunggu dropdown terbuka

    # Pilih opsi "100"
    option_100 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'v-list-item') and text()='100']"))
    )
    option_100.click()
    time.sleep(3)  # Tunggu halaman merefresh
    print("✅ Berhasil mengatur jumlah data per halaman menjadi 100!")
except Exception as e:
    print(f"⚠️ Gagal mengubah jumlah data per halaman: {e}")


# **7️⃣ Scraping Data Tabel & Paginasi**
count = 0  # Variabel untuk menghitung jumlah data yang diambil

with open(path + "/data_musrenbang2022.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["No", "Kelurahan", "rw", "kode","ukpd","permasalahan","template","tipe","status"])

    while True:
        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("tbody")

        for row in table.find_all("tr"):
            kelurahan_header = row.find("td", colspan="8")
            if kelurahan_header:
                current_kelurahan = kelurahan_header.text.strip()
                continue  # Lewati baris header dan lanjut ke data berikutnya
            
            cols = row.find_all("td")
            if len(cols) >= 9:
                rw = cols[1].text.strip()
                kode = cols[2].text.strip()
                ukpd = cols[3].text.strip()
                permasalahan = cols[4].text.strip()
                template = cols[5].text.strip()
                tipe = cols[6].text.strip()
                status = cols[8].text.strip()

                count += 1  # Tambahkan hitungan data
                print(f"[{count}] Kode: {kode} | UKPD: {ukpd} | Tipe: {tipe} | Status: {status}")  # Tampilan progress

                writer.writerow([count, current_kelurahan, rw, kode, ukpd, permasalahan, template, tipe, status])

        # **8️⃣ Cek & Klik Tombol "Next" Jika Ada**
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Halaman selanjutnya']"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)
        except:
            print(f"✅ Scraping selesai! Total data yang diambil: {count}")
            break

# **9️⃣ Tutup WebDriver**
driver.quit()
print("✅ Semua data disimpan di 'data_musrenbang.csv'.")
