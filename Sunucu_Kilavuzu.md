# 🎤 Proje Sunucusu ve Geliştirici Kılavuzu

Bu belge, "Kriptografi Terminali" projesinin teknik mimarisini kavramak, kurulumunu yapmak ve projeyi başkalarına sunarken sorulabilecek sorulara hazırlıklı olmak için hazırlanmıştır.

## 1. Teknik Kararlar ve Altyapı
- **Neden 79 Karakterlik Alfabe?**
  Hill şifrelemesi 2x2 matrislerle çalışır. Ancak şifrenin geri çözülebilmesi için determinantın alfabe uzunluğuna göre modüler tersinin alınabilmesi şarttır. Eğer alfabe 29 (sadece Türkçe harfler) veya 26 olsaydı, birçok matris geçersiz olurdu. Bu projede rakamlar, simgeler, ingilizce türkçe harfler kullanılmıstır. Ve 79 sayısına ulaşılmıştır. 79 asal bir sayı olduğu için Asal modüller matematiksel olarak her zaman tersine çevrilebilirdir. Bu sayede hata riski %0'a indirilmiştir.

- **Neden İki Farklı Python Çekirdeği?**
  1. **Saf Kütüphanesiz (`kutuphanesiz_versiyon.py`)**: Kriptografinin altında yatan for döngülerini, matris çarpımlarını ve modüler toplamayı en ilkel haliyle kavradığımızı kanıtlar.
  2. **NumPy Kütüphaneli (`kutuphaneli_versiyon.py`)**: Gerçek dünya projelerinde bu işlemlerin `np.dot` ile nasıl vektörel ve çok daha hızlı yapıldığını gösterir.

## 2. Kurulum ve Çalıştırma Adımları (Demo İçin)
Projeyi sunacağınız bilgisayarda şunları yapmanız yeterlidir:
1. `hill-vernam-cipher` klasörünü açın.
2. `çalıştır.bat` dosyasına çift tıklayın. (Bu dosya eksik modülleri `pip install flask numpy` ile kurar ve `app.py`'yi başlatır).
3. Tarayıcıyı açın ve adres çubuğuna `http://localhost:5000` yazın.

## 3. Sunum Sırasında Uygulanacak Demo Senaryosu
Sunum yaparken izleyiciyi etkilemek için şu adımları izleyebilirsiniz:
1. **Giriş:** "Saf Çekirdek" sekmesinde `help` yazıp enter'a basın. Sistem, yardım menüsünü ekrana basacaktır. Projenin ne yaptığını bu menü üzerinden okuyarak anlatabilirsiniz.
2. **Çift Çekirdek Gösterisi:** "ÇİFT ÇEKİRDEK" sekmesi ile iki ayrı algoritmayı aynı anda test edebilirsiniz.
3. **Kaynak Kod:** Kodları göstermek için IDE'ye (VSC vb.) dönmenize gerek yok. Doğrudan uygulamadaki "KAYNAK KODLAR" butonuna tıklayarak projenin kendi kaynak kodunu uygulamanın içinden gösterebilirsiniz.

