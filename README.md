# GameLingo Profiles

GameLingo'nun uygulamadan ayrı indirilen, sürümlü ve oyuna özgü Türkçe çeviri profilleri. **Profiller STT veya çeviri modeli değildir**: mikrofon sinyalini düzeltmezler ve Parakeet/Whisper/OPUS model dosyalarının yerine geçmezler.

## God of War Ragnarök v8

Bu sürümde tanınan karakter/yer/mitoloji adları, dövüş ve keşif terimleri, kısa Türkçe diyalog karşılıkları ve yalnızca hedefli oyun adı varyantları genişletildi. Önceki 3.621 SHA-256 diyalog parmak izi korunur. Parmak izleri, iki ASR motorunun **zaten duyduğunu iddia ettiği kelimeler** arasında seçim yapmak içindir; oyundan duyulmayan kelime veya replik üretmezler.

- **protected_names:** Karakter/yer/mitoloji özel adları. Yaygın İngilizce sözcükler burada mümkün olduğunca tutulmaz.
- **glossary:** Cümle içindeki oyun terimlerini çeviri öncesinde koruyan İngilizce–Türkçe karşılıklar. Buradaki Türkçe terimler GameLingo'nun tutarlılık tercihidir; tamamının oyunun resmî Türkçe yerelleştirmesi olduğu iddia edilmez.
- **translations:** Yalnızca tam cümle eşleşmesi veya uygulamanın sınırlı tek-kenar eksiltme kuralı ile kullanılan kısa diyalog çevirileri.
- **asr_aliases:** Tam token sınırlarıyla eşleşen, oyun profiline özgü yazım/ses çözümleme varyantları. Yaygın başka isimleri yeniden yazabilen `James -> Atreus` ve `fairies -> Faye` gibi riskli alias'lar kaldırıldı.
- **script_rescue_hashes:** Tam oyun metnini saklamadan kullanılan kelime dizisi parmak izleri.

Oyun terminolojisi için PlayStation'ın God of War Ragnarök oyun ve geliştirici yazıları, konuşma hataları için GameLingo'nun gerçek test kayıtları referans alınır. Yeni fonetik yazım varyantları, telefonda doğrulanana kadar yalnızca test adayıdır. Tam senaryo veya altyazı dökümü profillere topluca kopyalanmaz.

## Güvenli güncelleme

Uygulama katalogdaki `profile_version` arttığında yalnızca ilgili JSON profilini indirir; büyük model ZIP'i veya APK değişmez. Ses seviyesinde sorun, VAD'nin cümleyi hiç yakalayamaması ve iki ASR motorunun aynı kelimeyi yanlış tanıması tek başına profil büyüterek çözülemez.

Profil kalitesini ve sürüm–katalog uyumunu yerel olarak test et:

```bash
python3 -m unittest discover -s tests -v
```

Aynı kontroller `.github/workflows/validate-profiles.yml` ile profiller güncellendikçe otomatik olarak çalışır.
