# 🔐 Hill & Vernam Kriptografi Terminali

Klasik kriptografi yöntemleri olan **Hill Şifrelemesi** ve **Vernam (One Time Pad)** algoritmalarının modern, siberpunk ve retro terminal esintili bir web arayüzünde birleştirildiği tam donanımlı bir kriptografi laboratuvarıdır.

## ✨ Özellikler

- **Çift Çekirdekli Mimari:** İşlemler arka planda iki farklı şekilde hesaplanır:
  - **SAF Çekirdek:** Hiçbir dış bağımlılık olmadan (saf Python) matematiksel olarak yazılmış algoritmalar.
  - **NUMPY Çekirdek:** Python'un popüler veri bilimi kütüphanesi NumPy kullanılarak optimize edilmiş vektörel işlemler.
- **Canlı Sistem Doğrulaması:** "Çift Çekirdek" sekmesinde iki mimari yan yana çalışır ve sonuçların doğruluğu sistem tarafından otomatik teyit edilir.
- **Kaynak Kod Okuyucusu:** Uygulama içinden arka plandaki Python kodlarını okuyabilme imkanı.
- **Gelişmiş UX Deneyimi:** Nielsen ilkelerine uygun olarak tasarlanmış suni yükleme animasyonları, dinamik terminal genişliği ve yardım (`help`) komutları.

## 🚀 Kurulum ve Çalıştırma

Bilgisayarınızda Python yüklü olduğundan emin olun.

1. Projeyi bilgisayarınıza indirin (clone).
2. Proje dizinine girin ve `çalıştır.bat` dosyasına çift tıklayın.
3. Sistem gerekli kütüphaneleri (Flask, Numpy) otomatik olarak indirecek ve sunucuyu başlatacaktır.
4. Tarayıcınızda `http://localhost:5000` adresine giderek terminali kullanmaya başlayabilirsiniz.

## 🛠️ Kullanım İpuçları
- Terminal satırına şifrelemek istediğiniz metni yazıp `Enter`'a basın.
- **Komutlar:** 
  - `help` veya `yardim`: Sistem dokümantasyonunu gösterir.
  - `clear`: Terminali tamamen temizler.

## ⚙️ Teknik Detaylar
- **Alfabe:** 79 karakterlik genişletilmiş alfabe kullanılmıştır. 79 asal sayı olduğu için Hill matris çarpımlarında modüler tersinme işlemlerini hatasız garantiler.
- **Ön Yüz:** Vanilla JS, CSS (Glassmorphism & Cyberpunk) ve HTML.
- **Arka Yüz:** Python (Flask, NumPy).

Geliştirici: Ali Eren Tuğrul
