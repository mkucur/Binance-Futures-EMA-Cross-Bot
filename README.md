# Binance-Futures-EMA-Cross-Bot
# Binance Vadeli İşlemler Botu

Bu proje, Binance vadeli işlemler platformunda otomatik alım satım yapabilen bir Python botudur. Bot, EMA (Exponential Moving Average) kesişim stratejisini kullanarak alım ve satım kararları verir. Kullanıcılar, EMA değerlerini belirleyerek botun davranışını özelleştirebilirler. Alım satım market emir üzerinden gerçekleşir. 

## Kurulum

1. Python'u [python.org](https://www.python.org/) adresinden indirip kurun.
2. Gerekli kütüphaneleri yüklemek için terminal veya komut istemcisine şu komutu yazın:

## Kullanım

1. `main.py` dosyasını çalıştırarak programı başlatın:

    ```
    python main.py
    ```

2. Program, kullanıcıdan gerekli parametreleri (API anahtarı, API sırrı, EMA değerleri, vb.) isteyecektir.
3. Bot başlatıldığında, EMA kesişimlerine göre otomatik alım satım işlemleri gerçekleştirilecektir.

## Parametreler

- `API Anahtarı`: Binance hesabınıza erişim sağlamak için API anahtarınızı ekleyin.
- `API Sırrı`: Binance API anahtarınıza ait sırrı ekleyin.
- `EMA Değerleri`: Kullanıcı tarafından belirlenen EMA değerleri.
- `symbol` : işlem yapılacak hisse çifti
- `no_of_decimals`:fiyatın virgünden sonraki kısmı kaç rakam
- `volume` : işlem hacmi kasanın % kaçı
- `parite` : kaç dakikalık grafiklerde işlem yapılacak
- `ema_short` : kısa ema değeri
- `ema_long` : uzun ema değeri

## Katkıda Bulunma

1. Projeyi fork edin.
2. Yeni bir branch oluşturun: `git checkout -b yenifeature`
3. Yapmak istediğiniz değişiklikleri yapın.
4. Değişiklikleri commit edin: `git commit -m 'Yeni özellik ekle'`
5. Branch'i push edin: `git push origin yenifeature`
6. Bir Pull Request açın.

## Lisans

Bu proje [MIT lisansı](LICENSE) altında lisanslanmıştır. Detaylı bilgi için [LICENSE](LICENSE) dosyasını inceleyebilirsiniz.
