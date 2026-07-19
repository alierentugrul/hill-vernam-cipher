document.addEventListener('DOMContentLoaded', () => {
    const terminals = {
        kutuphanesiz: document.getElementById('term-kutuphanesiz'),
        kutuphaneli: document.getElementById('term-kutuphaneli'),
        ikisi: document.getElementById('term-ikisi'),
        ikisiLeft: document.getElementById('term-ikisi-left'),
        ikisiRight: document.getElementById('term-ikisi-right'),
        kaynak: document.getElementById('term-kaynak'),
        kaynakLeft: document.getElementById('term-kaynak-left'),
        kaynakRight: document.getElementById('term-kaynak-right')
    };

    const inputField = document.getElementById('cli-input');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const clearBtn = document.getElementById('clear-btn');

    let currentMode = 'kutuphanesiz';
    let sourceLoaded = false; // Kaynak kodların bir kez yüklenmesini takip eder

    function delay(ms) { return new Promise(res => setTimeout(res, ms)); }

    // Ekranı temizleme butonu
    clearBtn.addEventListener('click', () => {
        if (currentMode === 'ikisi') {
            terminals.ikisiLeft.innerHTML = '';
            terminals.ikisiRight.innerHTML = '';
        } else if (currentMode !== 'kaynak') {
            // Kaynak kod terminali temizlenmez
            terminals[currentMode].innerHTML = '';
        }
        inputField.focus();
    });

    // Sekme değiştirme mantığı
    tabBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const mode = btn.getAttribute('data-mode');
            currentMode = mode;
            
            // Bütün terminalleri gizle
            terminals.kutuphanesiz.style.display = 'none';
            terminals.kutuphaneli.style.display = 'none';
            terminals.ikisi.style.display = 'none';
            terminals.kaynak.style.display = 'none';

            // Seçileni göster
            terminals[mode].style.display = (mode === 'ikisi' || mode === 'kaynak') ? 'flex' : 'block';
            
            // Dinamik genişlik ayarı
            const appContainer = document.querySelector('.app-container');
            if (mode === 'ikisi' || mode === 'kaynak') {
                appContainer.classList.add('wide-mode');
            } else {
                appContainer.classList.remove('wide-mode');
            }
            
            // Placeholder ayarları ve Input Alanı Gizleme
            const inputAreaContainer = document.getElementById('input-area');
            if (mode === 'ikisi') {
                inputAreaContainer.style.display = 'flex';
                inputField.placeholder = "Şifrelenecek metni girin (İki terminalde de çalışacak)...";
                inputField.disabled = false;
            } else if (mode === 'kaynak') {
                inputAreaContainer.style.display = 'none';
                inputField.disabled = true;
                
                // Eğer kodlar daha önce yüklenmediyse otomatik yükle
                if (!sourceLoaded) {
                    sourceLoaded = true;
                    try {
                        const resSaf = await fetch('/api/source?mode=kutuphanesiz');
                        const dataSaf = await resSaf.json();
                        printCode(dataSaf.source, 'kaynak-left');

                        const resNumpy = await fetch('/api/source?mode=kutuphaneli');
                        const dataNumpy = await resNumpy.json();
                        printCode(dataNumpy.source, 'kaynak-right');
                    } catch (err) {
                        printLine("Kodlar yüklenirken hata oluştu.", "error-msg", 'kaynak-left');
                    }
                }
            } else {
                inputAreaContainer.style.display = 'flex';
                inputField.placeholder = "Şifrelenecek metni girin...";
                inputField.disabled = false;
            }
            
            if (!inputField.disabled) inputField.focus();
        });
    });

    // Terminale yazı yazdırma fonksiyonu
    function printLine(text, className = "output-line", targetMode = currentMode) {
        let target;
        if (targetMode === 'ikisi-left') target = terminals.ikisiLeft;
        else if (targetMode === 'ikisi-right') target = terminals.ikisiRight;
        else if (targetMode === 'kaynak-left') target = terminals.kaynakLeft;
        else if (targetMode === 'kaynak-right') target = terminals.kaynakRight;
        else target = terminals[targetMode];

        if (!target) return;

        const line = document.createElement('div');
        line.className = `output-line ${className}`;
        line.textContent = text;
        target.appendChild(line);
        // Otomatik aşağı kaydırma (scroll to bottom) kullanıcı isteğiyle kaldırıldı
    }
    
    // Terminale Kod yazdırma fonksiyonu (Prism.js ile)
    function printCode(codeText, targetMode = currentMode) {
        let target;
        if (targetMode === 'kaynak-left') target = terminals.kaynakLeft;
        else if (targetMode === 'kaynak-right') target = terminals.kaynakRight;
        else target = terminals[targetMode];

        const pre = document.createElement('pre');
        const code = document.createElement('code');
        code.className = 'language-python';
        code.textContent = codeText;
        pre.appendChild(code);
        target.appendChild(pre);
        Prism.highlightElement(code);
        target.scrollTop = 0; // Kaynak kod okuyucu her zaman en üstte kalmalı
    }

    function printDict(dict, targetMode) {
        printLine(`Orijinal Metin: ${dict.orijinal_metin}`, "output-line", targetMode);
        printLine(`Sayısal Karşılıklar: [${dict.sayisal_karsiliklar.join(", ")}]`, "output-line", targetMode);
        printLine(`--- HILL ŞİFRELEME ---`, "header-msg", targetMode);
        printLine(`Hill Şifreli Sayılar: [${dict.hill_sifreli_sayilar.join(", ")}]`, "output-line", targetMode);
        printLine(`Hill Şifreli Metin: ${dict.hill_sifreli_metin}`, "output-line", targetMode);
        printLine(`--- VERNAM ŞİFRELEME ---`, "header-msg", targetMode);
        printLine(`Vernam Şifreli Sayılar: [${dict.vernam_sifreli_sayilar.join(", ")}]`, "output-line", targetMode);
        printLine(`Tam Şifreli Metin: ${dict.tam_sifreli_metin}`, "output-line", targetMode);
        printLine(`--- DEŞİFRELEME (ÇÖZME) ---`, "header-msg", targetMode);
        printLine(`Adım 1 (Vernam): [${dict.adim1_vernam_cozulmus_sayilar.join(", ")}] -> ${dict.adim1_vernam_cozulmus_metin}`, "output-line", targetMode);
        printLine(`Adım 2 (Hill): [${dict.adim2_hill_cozulmus_sayilar.join(", ")}] -> ${dict.adim2_hill_cozulmus_metin_padli} (Paddingli)`, "output-line", targetMode);
        printLine(`NİHAİ ÇÖZÜLMÜŞ METİN: ${dict.nihai_cozulmus_metin}`, "system-msg", targetMode);
    }

    function printHelp(targetMode) {
        printLine(">>> SİSTEM YARDIM DOKÜMANTASYONU <<<", "header-msg", targetMode);
        printLine("Bu sistem, Klasik Kriptografi yöntemleri olan Hill ve Vernam (OTP) şifrelemelerini kullanır.", "system-msg", targetMode);
        printLine("1. HILL ŞİFRELEMESİ:", "prompt", targetMode);
        printLine("2x2'lik bir anahtar matrisi kullanılarak metin 2'şerli bloklar halinde matris çarpımına sokulur. Asal değerli mod (79) algoritmayı güvende tutar.", "output-line", targetMode);
        printLine("2. VERNAM ŞİFRELEMESİ:", "prompt", targetMode);
        printLine("Hill çıktısı, 'gizlisifremiz' anahtarıyla XOR benzeri modüler toplama işlemine tabi tutularak ikinci bir güvenlik katmanı oluşturulur.", "output-line", targetMode);
        printLine("---", "output-line", targetMode);
        printLine("EK KOMUTLAR:", "header-msg", targetMode);
        printLine("- clear : Ekranı tamamen temizler.", "output-line", targetMode);
        printLine("- help  : Bu yardım menüsünü açar.", "output-line", targetMode);
    }

    // Input gönderme
    inputField.addEventListener('keypress', async (e) => {
        if (e.key === 'Enter') {
            const text = inputField.value.trim();
            if (!text) return;
            
            inputField.value = '';
            
            if (currentMode === 'ikisi') {
                printLine(`kullanici@kripto:~$ ${text}`, "prompt", 'ikisi-left');
                printLine(`kullanici@kripto:~$ ${text}`, "prompt", 'ikisi-right');
            } else {
                printLine(`kullanici@kripto:~$ ${text}`, "prompt", currentMode);
            }

            if (text.toLowerCase() === 'clear') {
                clearBtn.click();
                return;
            }

            if (text.toLowerCase() === 'help' || text.toLowerCase() === 'yardim' || text.toLowerCase() === 'yardım') {
                if (currentMode === 'ikisi') {
                    printHelp('ikisi-left');
                    printHelp('ikisi-right');
                } else {
                    printHelp(currentMode);
                }
                return;
            }

            // Animasyonlu işlem bekleme simülasyonu
            if (currentMode !== 'kaynak') {
                if (currentMode === 'ikisi') {
                    printLine("[*] Şifreleme çekirdeği başlatılıyor...", "system-msg", 'ikisi-left');
                    printLine("[*] Şifreleme çekirdeği başlatılıyor...", "system-msg", 'ikisi-right');
                    await delay(400);
                    printLine("[*] Matris ve anahtar değerleri hesaplanıyor...", "system-msg", 'ikisi-left');
                    printLine("[*] Matris ve anahtar değerleri hesaplanıyor...", "system-msg", 'ikisi-right');
                    await delay(300);
                } else {
                    printLine("[*] Şifreleme çekirdeği başlatılıyor...", "system-msg", currentMode);
                    await delay(400);
                    printLine("[*] Matris ve anahtar değerleri hesaplanıyor...", "system-msg", currentMode);
                    await delay(300);
                }
            }

            // Şifreleme isteği
            try {
                const res = await fetch('/api/encrypt', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text, mode: currentMode })
                });
                
                const data = await res.json();
                
                if (data.error) {
                    if (currentMode === 'ikisi') {
                        printLine(`HATA: ${data.error}`, "error-msg", 'ikisi-left');
                        printLine(`HATA: ${data.error}`, "error-msg", 'ikisi-right');
                    } else {
                        printLine(`HATA: ${data.error}`, "error-msg", currentMode);
                    }
                    return;
                }

                if (data.ikili_mod) {
                    printLine("=== [SAF KÜTÜPHANESİZ ÇEKİRDEK] ===", "header-msg", 'ikisi-left');
                    printDict(data.kutuphanesiz, 'ikisi-left');
                    
                    printLine("=== [NUMPY ÇEKİRDEK] ===", "header-msg", 'ikisi-right');
                    printDict(data.kutuphaneli, 'ikisi-right');
                    
                    if (data.kutuphanesiz.tam_sifreli_metin === data.kutuphaneli.tam_sifreli_metin) {
                        const msg = ">>> SİSTEM DOĞRULAMASI BAŞARILI: İki algoritma da aynı sonucu üretti.";
                        printLine(msg, "system-msg", 'ikisi-left');
                        printLine(msg, "system-msg", 'ikisi-right');
                    }
                } else {
                    printDict(data, currentMode);
                }
            } catch (err) {
                if (currentMode === 'ikisi') {
                    printLine("Sunucuya bağlanılamadı.", "error-msg", 'ikisi-left');
                    printLine("Sunucuya bağlanılamadı.", "error-msg", 'ikisi-right');
                } else {
                    printLine("Sunucuya bağlanılamadı.", "error-msg", currentMode);
                }
            }
        }
    });
});
