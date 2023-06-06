import requests
from bs4 import BeautifulSoup
import pandas as pd

# Dosya adı
urun_dosyasi = "urun.txt"

# Metin dosyasından URL'leri oku
with open(urun_dosyasi, "r") as dosya:
    urun_url_listesi = dosya.read().splitlines()

# Veri çerçevesini oluştur
veri = []

# Her bir URL için verileri al
for url in urun_url_listesi:
    sayfa = requests.get(url)
    soup = BeautifulSoup(sayfa.content, "html.parser")

    # Ürün adını al
    urun_adi_elementi = soup.find("div", class_="ProductName")
    if urun_adi_elementi:
        urun_adi = urun_adi_elementi.find("h1").text.strip()
        urun_kodu_elementi = urun_adi_elementi.find("span", class_="productcode")
        if urun_kodu_elementi:
            urun_kodu = urun_kodu_elementi.text.strip()
            urun_adi = urun_adi.replace(urun_kodu, "")
        urun_adi = urun_adi.strip()
    else:
        urun_adi = "N/A"

    # Fiyatı al
    fiyat_elementi = soup.find("span", class_="spanFiyat")
    if fiyat_elementi:
        fiyat = fiyat_elementi.text.strip()
        fiyat = fiyat.replace("₺", "").replace(".", "").replace(",", ".").strip()
    else:
        fiyat = "N/A"

    # %10 indirimli fiyatı hesapla
    if fiyat != "N/A":
        indirimli_fiyat = float(fiyat) * 0.9
        indirimli_fiyat = "{:.2f}".format(indirimli_fiyat).replace(".", ",")
        indirimli_fiyat = indirimli_fiyat.replace(",", ".")
    else:
        indirimli_fiyat = "N/A"

    # Verileri veri listesine ekle
    veri.append([urun_adi, fiyat, indirimli_fiyat])

# Veri çerçevesini oluştur
veri_cercevesi = pd.DataFrame(veri, columns=["Ürün Adı", "Site Satış Fiyatı", "%10 İndirimli Fiyat"])

# Verileri ekrana yazdır
print(veri_cercevesi)

# Verileri Excel dosyasına yaz
excel_dosyasi = "daiwagucelle.xlsx"
veri_cercevesi.to_excel(excel_dosyasi, index=False)
print("Veriler başarıyla '{}' dosyasına aktarıldı.".format(excel_dosyasi))
