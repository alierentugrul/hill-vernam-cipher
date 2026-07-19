# -*- coding: utf-8 -*-

"""
Hill ve Vernam Şifreleme (Kütüphanesiz Saf Python Versiyonu)
Alfabe: 79 Karakterli Özel Alfabe (Büyük/Küçük Harf, Rakam, Noktalama)
"""

ALFABE = "abcçdefgğhıijklmnoöprsştuüvyzqwxABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZQWX .,?!0123456789"
MOD = len(ALFABE) # 79 (Asal sayı olması matris tersini bulmada büyük avantajdır)

def harf_to_index(harf):
    """Harfin alfabedeki indeksini bulur."""
    return ALFABE.index(harf)

def index_to_harf(index):
    """İndekse karşılık gelen harfi döndürür."""
    return ALFABE[index % MOD]

def metin_to_sayi(metin):
    """Metni sayılardan oluşan bir listeye çevirir. Boşlukları ve bilinmeyenleri atar."""
    return [harf_to_index(h) for h in metin if h in ALFABE]

def mod_ters(a, m):
    """Modüler çarpma tersini bulur (a^-1 mod m)."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

class HillCipher:
    def __init__(self, matris):
        """2x2 bir anahtar matrisi alır. Örn: [[3, 3], [2, 5]]"""
        self.K = matris
        # Determinant hesabı: ad - bc
        self.det = (self.K[0][0] * self.K[1][1]) - (self.K[0][1] * self.K[1][0])
        self.det = self.det % MOD
        
        self.det_ters = mod_ters(self.det, MOD)
        if self.det_ters is None:
            raise ValueError(f"Bu matrisin {MOD} modunda tersi yok, başka bir anahtar seçin!")
            
        # Ters Matris Hesabı (Adjoint * Det_Ters mod 29)
        self.K_ters = [
            [(self.K[1][1] * self.det_ters) % MOD, (-self.K[0][1] * self.det_ters) % MOD],
            [(-self.K[1][0] * self.det_ters) % MOD, (self.K[0][0] * self.det_ters) % MOD]
        ]

    def sifrele(self, sayilar):
        # Eğer tek sayıda harf varsa, sonuna 'a' (0) ekleyerek çift yapalım
        if len(sayilar) % 2 != 0:
            sayilar.append(0)
            
        sifreli_sayilar = []
        for i in range(0, len(sayilar), 2):
            p1 = sayilar[i]
            p2 = sayilar[i+1]
            
            # Matris çarpımı: [K] * [P]
            c1 = (self.K[0][0] * p1 + self.K[0][1] * p2) % MOD
            c2 = (self.K[1][0] * p1 + self.K[1][1] * p2) % MOD
            sifreli_sayilar.extend([c1, c2])
            
        return sifreli_sayilar

    def sifre_coz(self, sayilar):
        cozulmus_sayilar = []
        for i in range(0, len(sayilar), 2):
            c1 = sayilar[i]
            c2 = sayilar[i+1]
            
            # Matris çarpımı: [K_ters] * [C]
            p1 = (self.K_ters[0][0] * c1 + self.K_ters[0][1] * c2) % MOD
            p2 = (self.K_ters[1][0] * c1 + self.K_ters[1][1] * c2) % MOD
            cozulmus_sayilar.extend([p1, p2])
            
        return cozulmus_sayilar

class VernamCipher:
    def __init__(self, anahtar_metin):
        self.anahtar_sayilar = metin_to_sayi(anahtar_metin)

    def anahtar_esitle(self, uzunluk):
        """Anahtarı metin uzunluğuna eşitler (uzatır veya kırpar)."""
        genisletilmis = []
        for i in range(uzunluk):
            genisletilmis.append(self.anahtar_sayilar[i % len(self.anahtar_sayilar)])
        return genisletilmis

    def sifrele(self, sayilar):
        anahtar = self.anahtar_esitle(len(sayilar))
        sifreli = []
        for p, k in zip(sayilar, anahtar):
            sifreli.append((p + k) % MOD)
        return sifreli

    def sifre_coz(self, sayilar):
        anahtar = self.anahtar_esitle(len(sayilar))
        cozulmus = []
        for c, k in zip(sayilar, anahtar):
            cozulmus.append((c - k) % MOD)
        return cozulmus
def web_icin_sifrele(orijinal_metin):
    """Web arayüzünden gelen metinleri şifreleyip detaylı JSON formatında döndürür."""
    sayisal_metin = metin_to_sayi(orijinal_metin)
    if not sayisal_metin:
        return {"error": "Geçerli bir harf girmediniz. Lütfen tekrar deneyin."}
        
    hill = HillCipher([[3, 3], [2, 5]])
    hill_sifreli_sayilar = hill.sifrele(sayilar=sayisal_metin.copy())
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
        print("--- 1. BAŞLANGIÇ ---")
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

        # --- HILL ŞİFRELEME ---
        print("--- 2. HILL ŞİFRELEME (1. Aşama) ---")
        hill_anahtari = [[3, 3], [2, 5]]
        hill = HillCipher(hill_anahtari)
        
        hill_sifreli_sayilar = hill.sifrele(sayilar=sayisal_metin.copy())
        hill_sifreli_metin = "".join(index_to_harf(s) for s in hill_sifreli_sayilar)
        print("Hill Şifreli Sayılar:", hill_sifreli_sayilar)
        print("Hill Şifreli Metin:", hill_sifreli_metin)
        print("-" * 30)

        # --- VERNAM ŞİFRELEME ---
        print("--- 3. VERNAM ŞİFRELEME (2. Aşama) ---")
        vernam_anahtar_kelimesi = "gizlisifremiz"
        vernam = VernamCipher(vernam_anahtar_kelimesi)
        
        vernam_sifreli_sayilar = vernam.sifrele(hill_sifreli_sayilar)
        tam_sifreli_metin = "".join(index_to_harf(s) for s in vernam_sifreli_sayilar)
        print("Vernam (Tam) Şifreli Sayılar:", vernam_sifreli_sayilar)
        print("Tam Şifreli Metin (Hill + Vernam):", tam_sifreli_metin)
        print("-" * 30)

        # --- DEŞİFRELEME İŞLEMİ (Sırasıyla: Vernam Çöz -> Hill Çöz) ---
        print("--- 4. DEŞİFRELEME İŞLEMİ ---")
        
        # Önce Vernam çözülür
        vernam_cozulmus_sayilar = vernam.sifre_coz(vernam_sifreli_sayilar)
        vernam_cozulmus_metin = "".join(index_to_harf(s) for s in vernam_cozulmus_sayilar)
        print("Adım 1: Vernam Çözülmüş Sayılar:", vernam_cozulmus_sayilar)
        print("Adım 1: Vernam Çözülmüş (Hill Şifreli) Metin:", vernam_cozulmus_metin)
        print("-" * 20)
        
        # Sonra Hill çözülür
        hill_cozulmus_sayilar = hill.sifre_coz(vernam_cozulmus_sayilar)
        
        cozulmus_metin_padli = "".join(index_to_harf(s) for s in hill_cozulmus_sayilar)
        print("Adım 2: Hill Çözülmüş Sayılar:", hill_cozulmus_sayilar)
        print("Adım 2: Hill Çözülmüş Metin (Padding Dahil):", cozulmus_metin_padli)
        print("-" * 20)
        
        # Eklenen 'a' (padding) harfini orijinal uzunluğa göre temizle
        cozulmus_metin = cozulmus_metin_padli[:len(sayisal_metin)]
        
        print("NİHAİ ÇÖZÜLMÜŞ METİN (Padding Temizlenmiş):", cozulmus_metin)
