# 🎤 Proje Sunucusu ve Geliştirici Kılavuzu

Bu belge, "Kriptografi Terminali" projesinin teknik mimarisini kavramak, kurulumunu yapmak ve projeyi başkalarına (jüri, akademisyen veya öğrenciler) sunarken sorulabilecek sorulara hazırlıklı olmak için hazırlanmıştır.

## 1. Projenin Çıkış Noktası ve Amacı
Bu proje sadece iki şifreleme algoritmasının kodunu yazıp geçmek yerine, **Kullanıcı Deneyimi (UX)** ve **Yazılım Mimarisi** ilkelerinin gözetildiği bir "ürün" ortaya koymak amacıyla geliştirilmiştir. Konsolda çalışan siyah ekranlı bir betik yerine; siberpunk hissi veren, kendi animasyonları olan ve aynı anda iki farklı yazılım mimarisini test edip karşılaştıran interaktif bir platform hedeflenmiştir.

## 2. Teknik Kararlar ve Altyapı
- **Neden 79 Karakterlik Alfabe?**
  Hill şifrelemesi 2x2 matrislerle çalışır. Ancak şifrenin geri çözülebilmesi için determinantın alfabe uzunluğuna göre modüler tersinin alınabilmesi şarttır. Eğer alfabe 29 (sadece Türkçe harfler) veya 26 olsaydı, birçok matris geçersiz olurdu. 79 asal bir sayıdır. Asal modüller matematiksel olarak her zaman tersine çevrilebilirdir. Bu sayede hata riski %0'a indirilmiştir.

- **Neden İki Farklı Python Çekirdeği?**
  1. **Saf Kütüphanesiz (`kutuphanesiz_versiyon.py`)**: Kriptografinin altında yatan for döngülerini, matris çarpımlarını ve modüler toplamayı en ilkel haliyle kavradığımızı kanıtlar.
  2. **NumPy Kütüphaneli (`kutuphaneli_versiyon.py`)**: Gerçek dünya projelerinde bu işlemlerin `np.dot` ile nasıl vektörel ve çok daha hızlı yapıldığını gösterir.

## 3. Kurulum ve Çalıştırma Adımları (Demo İçin)
Projeyi sunacağınız bilgisayarda şunları yapmanız yeterlidir:
1. `hill-vernam-cipher` klasörünü açın.
2. `çalıştır.bat` dosyasına çift tıklayın. (Bu dosya eksik modülleri `pip install flask numpy` ile kurar ve `app.py`'yi başlatır).
3. Tarayıcıyı açın ve adres çubuğuna `http://localhost:5000` yazın.

## 4. Sunum Sırasında Uygulanacak Demo Senaryosu
Sunum yaparken izleyiciyi etkilemek için şu adımları izleyebilirsiniz:
1. **Giriş:** "Saf Çekirdek" sekmesinde `help` yazıp enter'a basın. Sistem yardım menüsünü ekrana basacaktır. Projenin ne yaptığını bu menü üzerinden okuyarak anlatın.
2. **Animasyonlar:** Herhangi bir şifreleme yapın. Sistemin bilerek beklediği ("Çekirdek başlatılıyor...") kısımları göstererek, bunun bir UX kararı (Nielsen Heuristikleri: Sistem Durumu Görünürlüğü) olduğunu belirtin.
3. **Çift Çekirdek Gösterisi:** "ÇİFT ÇEKİRDEK" sekmesine geçin. Bir kelime yazın ve arka planda çalışan iki ayrı algoritmanın aynı anda ekrana nasıl farklı mimarilerle aynı sonucu bastığını ve "SİSTEM DOĞRULAMASI BAŞARILI" mesajını gösterin.
4. **Şeffaflık (Kaynak Kod):** Kodları göstermek için IDE'ye (VSC vb.) dönmeyin. Doğrudan uygulamadaki "KAYNAK KODLAR" butonuna tıklayarak projenin kendi kaynak kodunu uygulamanın içinden okutabildiğini gösterin.

Bu rehberi projeyi savunurken ve anlatırken bir "kopya kağıdı" olarak kullanabilirsiniz. Başarılar!
