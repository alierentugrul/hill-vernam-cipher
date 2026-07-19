# -*- coding: utf-8 -*-

"""
Hill ve Vernam Şifreleme (Kütüphaneli Versiyon - NumPy)
Alfabe: 79 Karakterli Özel Alfabe (Büyük/Küçük Harf, Rakam, Noktalama)
"""

import numpy as np

ALFABE = "abcçdefgğhıijklmnoöprsştuüvyzqwxABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWX .,?!0123456789"
MOD = len(ALFABE) # 79

def harf_to_index(harf):
    return ALFABE.index(harf)

def index_to_harf(index):
    return ALFABE[int(index) % MOD]

def metin_to_sayi(metin):
    return [harf_to_index(h) for h in metin if h in ALFABE]

def mod_ters(a, m):
    """Modüler çarpma tersini bulur (a^-1 mod m)."""
    a = int(a) % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

class HillCipher:
    def __init__(self, matris):
        # Numpy array olarak tanımlıyoruz
        self.K = np.array(matris)
        
        # Numpy ile determinant hesaplama (Yuvarlama hatalarını önlemek için round ve int kullanıyoruz)
        self.det = int(round(np.linalg.det(self.K)))
        self.det = self.det % MOD
        
        self.det_ters = mod_ters(self.det, MOD)
        if self.det_ters is None:
            raise ValueError(f"Bu matrisin {MOD} modunda tersi yok!")
            
        # 2x2 matris için Numpy olmadan da kolayca adjoint bulunabilir ama 
        # Numpy kütüphanesini göstermek adına matris işlemleri:
        adjoint = np.array([
            [self.K[1][1], -self.K[0][1]],
            [-self.K[1][0], self.K[0][0]]
        ])
        
        # Ters Matris = Adjoint * Det_Ters mod 29
        self.K_ters = (adjoint * self.det_ters) % MOD

    def sifrele(self, sayilar):
        if len(sayilar) % 2 != 0:
            sayilar.append(0)
            
        sifreli_sayilar = []
        for i in range(0, len(sayilar), 2):
            vektor = np.array([sayilar[i], sayilar[i+1]])
            
            # Numpy nokta çarpımı (dot product) kullanılarak matris çarpımı
            sonuc_vektor = np.dot(self.K, vektor) % MOD
            sifreli_sayilar.extend(sonuc_vektor.tolist())
            
        return sifreli_sayilar

    def sifre_coz(self, sayilar):
        cozulmus_sayilar = []
        for i in range(0, len(sayilar), 2):
            vektor = np.array([sayilar[i], sayilar[i+1]])
            
            # Numpy ile ters matris çarpımı
            sonuc_vektor = np.dot(self.K_ters, vektor) % MOD
            cozulmus_sayilar.extend(sonuc_vektor.tolist())
            
        return cozulmus_sayilar

class VernamCipher:
    def __init__(self, anahtar_metin):
        self.anahtar_sayilar = np.array(metin_to_sayi(anahtar_metin))

    def anahtar_esitle(self, uzunluk):
        # Numpy kütüphanesi ile anahtarı metin uzunluğuna kadar tekrarlatıyoruz
        tekrar_sayisi = (uzunluk // len(self.anahtar_sayilar)) + 1
        genisletilmis = np.tile(self.anahtar_sayilar, tekrar_sayisi)[:uzunluk]
        return genisletilmis

    def sifrele(self, sayilar):
        vektor_sayilar = np.array(sayilar)
        vektor_anahtar = self.anahtar_esitle(len(sayilar))
        
        # Numpy vektör toplama işlemi (For döngüsü kullanmaya gerek kalmaz)
        sifreli = (vektor_sayilar + vektor_anahtar) % MOD
        return sifreli.tolist()

    def sifre_coz(self, sayilar):
        vektor_sayilar = np.array(sayilar)
        vektor_anahtar = self.anahtar_esitle(len(sayilar))
        
        # Numpy vektör çıkarma işlemi
        cozulmus = (vektor_sayilar - vektor_anahtar) % MOD
        return cozulmus.tolist()

def web_icin_sifrele(orijinal_metin):
    sayisal_metin = metin_to_sayi(orijinal_metin)
    if not sayisal_metin:
        return {"error": "Geçerli bir harf girmediniz. Lütfen tekrar deneyin."}
        
    hill = HillCipher([[3, 3], [2, 5]])
    hill_sifreli_sayilar = hill.sifrele(sayisal_metin.copy())
    hill_sifreli_metin = "".join(index_to_harf(s) for s in hill_sifreli_sayilar)
    
    vernam = VernamCipher("gizlisifremiz")
    vernam_sifreli_sayilar = vernam.sifrele(hill_sifreli_sayilar)
    tam_sifreli_metin = "".join(index_to_harf(s) for s in vernam_sifreli_sayilar)
    
    vernam_cozulmus_sayilar = vernam.sifre_coz(vernam_sifreli_sayilar)
    vernam_cozulmus_metin = "".join(index_to_harf(s) for s in vernam_cozulmus_sayilar)
    
    hill_cozulmus_sayilar = hill.sifre_coz(vernam_cozulmus_sayilar)
    cozulmus_metin_padli = "".join(index_to_harf(s) for s in hill_cozulmus_sayilar)
    cozulmus_metin = cozulmus_metin_padli[:len(sayisal_metin)]
    
    return {
        "orijinal_metin": orijinal_metin,
        "sayisal_karsiliklar": sayisal_metin,
        "hill_sifreli_sayilar": hill_sifreli_sayilar,
        "hill_sifreli_metin": hill_sifreli_metin,
        "vernam_sifreli_sayilar": vernam_sifreli_sayilar,
        "tam_sifreli_metin": tam_sifreli_metin,
        "adim1_vernam_cozulmus_sayilar": vernam_cozulmus_sayilar,
        "adim1_vernam_cozulmus_metin": vernam_cozulmus_metin,
        "adim2_hill_cozulmus_sayilar": hill_cozulmus_sayilar,
        "adim2_hill_cozulmus_metin_padli": cozulmus_metin_padli,
        "nihai_cozulmus_metin": cozulmus_metin
    }

if __name__ == "__main__":
    while True:
        print("\n" + "="*40)
        print("--- NUMPY (KÜTÜPHANELİ) VERSİYON ---")
        orijinal_metin = input("Lütfen şifrelenecek metni girin (Çıkmak için 'q' veya 'cikis' yazın): ")
        
        if orijinal_metin.strip().lower() in ['q', 'cikis', 'çıkış', 'exit', 'quit']:
            print("Çıkış yapılıyor. İyi günler!")
            break
            
        print("Orijinal Metin:", orijinal_metin)
        
        sayisal_metin = metin_to_sayi(orijinal_metin)
        if not sayisal_metin:
            print("Geçerli bir harf girmediniz. Lütfen tekrar deneyin.")
            continue
            
        print("Sayısal Karşılıklar:", sayisal_metin)
        print("-" * 30)
        
        # --- 1. HILL ŞİFRELEME ---
        print("--- 2. HILL ŞİFRELEME (1. Aşama) ---")
        hill = HillCipher([[3, 3], [2, 5]])
        hill_sifreli_sayilar = hill.sifrele(sayisal_metin.copy())
        hill_sifreli_metin = "".join(index_to_harf(s) for s in hill_sifreli_sayilar)
        
        print("Hill Şifreli Sayılar:", hill_sifreli_sayilar)
        print("Hill Şifreli Metin:", hill_sifreli_metin)
        print("-" * 30)
        
        # --- 2. VERNAM ŞİFRELEME ---
        print("--- 3. VERNAM ŞİFRELEME (2. Aşama) ---")
        vernam = VernamCipher("gizlisifremiz")
        tam_sifreli_sayilar = vernam.sifrele(hill_sifreli_sayilar)
        
        print("Vernam (Tam) Şifreli Sayılar:", tam_sifreli_sayilar)
        print("Tam Şifreli Metin (Hill + Vernam):", "".join(index_to_harf(s) for s in tam_sifreli_sayilar))
        print("-" * 30)
        
        # --- DEŞİFRELEME ---
        print("--- 4. DEŞİFRELEME İŞLEMİ ---")
        vernam_cozulen = vernam.sifre_coz(tam_sifreli_sayilar)
        print("Adım 1: Vernam Çözülmüş Sayılar:", vernam_cozulen)
        print("Adım 1: Vernam Çözülmüş (Hill Şifreli) Metin:", "".join(index_to_harf(s) for s in vernam_cozulen))
        print("-" * 20)
        
        hill_cozulen = hill.sifre_coz(vernam_cozulen)
        cozulmus_metin_padli = "".join(index_to_harf(s) for s in hill_cozulen)
        
        print("Adım 2: Hill Çözülmüş Sayılar:", hill_cozulen)
        print("Adım 2: Hill Çözülmüş Metin (Padding Dahil):", cozulmus_metin_padli)
        print("-" * 20)
        
        # Eklenen 'a' (padding) harfini orijinal uzunluğa göre temizle
        cozulmus_metin = cozulmus_metin_padli[:len(sayisal_metin)]
        
        print("NİHAİ ÇÖZÜLMÜŞ METİN (Padding Temizlenmiş):", cozulmus_metin)
