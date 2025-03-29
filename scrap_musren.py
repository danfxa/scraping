#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 01:24:13 2025

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
import argparse

# Argument Parser
parser = argparse.ArgumentParser(description="Scrape data musrenbang berdasarkan ID range")
parser.add_argument("a", type=int, help="Part")
#parser.add_argument("initial",type = int, help = "Nilai awal")
#parser.add_argument("step",type = int, help = "Step")
args = parser.parse_args()
# **Setup WebDriver**
options = webdriver.ChromeOptions()
options.add_argument("--remote-debugging-port=9224")
options.add_argument("--user-data-dir=/tmp/chrome-profile-2")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
start_time = time.time()

step = 3000
a = args.a
init_page = 8009300+a*step  # Halaman awal
end_page = init_page +step # Halaman akhir
count = 0

path = "/Users/dprddkijakarta/Documents/scraping/scraping/data/musrenbang"
# **Buka File CSV untuk Menyimpan Data**
with open(path+"/data_musrenbang_p"+str(a)+".csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "No", "Kode Tracking", "Isu", "Permasalahan", "Kelurahan", "RW", "RT",
        "Prioritas Kelurahan", "Prioritas Kecamatan", "Usulan Kegiatan", "Definisi Operasional",
        "Syarat dan Ketentuan", "Volume Satuan", "Tipe Usulan", "Status Data",
        "Hasil Validasi Kelurahan", "Catatan Kelurahan", "Divalidasi Kelurahan",
        "Hasil Validasi Kecamatan", "Catatan Kecamatan", "Divalidasi Kecamatan",
        "Unit Kerja APBD", "Status APBD", "Sub Kegiatan"
    ])


    for i in range(init_page, end_page):
        url = f"https://musrenbang.jakarta.go.id/public_musrenbang/{i}/home"

        for attempt in range(3):  # Retry sampai 3 kali jika error
            try:
                driver.get(url)
                time.sleep(1)

                # **Ambil Data Detail**
                soup = BeautifulSoup(driver.page_source, "html.parser")

                def get_detail(label):
                    """Mengambil data dari elemen HTML berdasarkan label v-subheader."""
                    try:
                        element = soup.find("div", class_="v-subheader", string=label)
                        if element:
                            parent_div = element.find_parent("div")
                            if parent_div:
                                next_div = parent_div.find_next_sibling("div")
                                if next_div:
                                    value_element = next_div.find("div", class_="v-card__text")
                                    return value_element.text.strip() if value_element else "Tidak Ada Data"
                        return "Tidak Ada Data"
                    except:
                        return "Tidak Ada Data"

                kode_tracking = get_detail("Kode Tracking")
                isu = get_detail("Isu")
                permasalahan = get_detail("Permasalahan")
                kelurahan = get_detail("Kelurahan")
                rw = get_detail("RW")
                rt = get_detail("RT")
                prioritas_kelurahan = get_detail("Prioritas Kelurahan")
                prioritas_kecamatan = get_detail("Prioritas Kecamatan")
                usulan_kegiatan = get_detail("Usulan Kegiatan")
                definisi_operasional = get_detail("Definisi Operasional")
                syarat_ketentuan = get_detail("Syarat dan Ketentuan")
                volume_satuan = get_detail("Volume Satuan")
                tipe_usulan = get_detail("Tipe Usulan")

                # **Ambil Status Validasi**
                status_data = get_detail("Status Data")
                hasil_validasi_kelurahan = get_detail("[KELURAHAN] Hasil Validasi")
                catatan_kelurahan = get_detail("[KELURAHAN] Catatan Validasi")
                divalidasi_kelurahan = get_detail("[KELURAHAN] Divalidasi oleh")
                hasil_validasi_kecamatan = get_detail("[KECAMATAN] Hasil Validasi")
                catatan_kecamatan = get_detail("[KECAMATAN] Catatan Validasi")
                divalidasi_kecamatan = get_detail("[KECAMATAN] Divalidasi oleh")

                # **Ambil Data APBD**
                unit_kerja_apbd = get_detail("Unit Kerja")
                status_apbd = get_detail("Status")
                sub_kegiatan = get_detail("Sub Kegiatan")

                count += 1
                est = ((time.time()-start_time)/count*(end_page-(init_page+count)))/60
                print(f"estimasi selesai: {est}")
                print(f"[{count}/{end_page - init_page}] ✅ {kode_tracking} | {usulan_kegiatan} | {status_data}")
                
                if not kode_tracking:
                    continue
                writer.writerow([
                    count, kode_tracking, isu, permasalahan, kelurahan, rw, rt,
                    prioritas_kelurahan, prioritas_kecamatan, usulan_kegiatan, definisi_operasional,
                    syarat_ketentuan, volume_satuan, tipe_usulan, status_data,
                    hasil_validasi_kelurahan, catatan_kelurahan, divalidasi_kelurahan,
                    hasil_validasi_kecamatan, catatan_kecamatan, divalidasi_kecamatan,
                    unit_kerja_apbd, status_apbd, sub_kegiatan
                ])
                
                break  # Jika scraping berhasil, keluar dari loop retry
            except Exception as e:
                print(f"⚠️ Gagal scraping halaman {i}, percobaan {attempt+1}/3. Error: {e}")
                time.sleep(3)  # Tunggu sebentar sebelum mencoba ulang

# **Tutup WebDriver**
driver.quit()
print("✅ Semua data disimpan di 'data_musrenbang.csv'.")
