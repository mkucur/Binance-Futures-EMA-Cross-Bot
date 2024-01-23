from binance.client import Client
import pandas as pd

api = "api"
api_secret = "api_secret"

# Binance müşteri oluştuuyoruz.

client = Client(api,api_secret,tld="com",testnet=True) # testnet dışına çıkacaksak testnet = false yapalım

class Bot:
    """
    symbol : işlem yapılacak hisse çifti
    no_of_decimals:fiyatın virgünden sonraki kısmı kaç rakam
    volume : işlem hacmi kasanın % kaçı
    parite : kaç dakikalık grafiklerde işlem yapılacak
    ema_short : kısa ema değeri
    ema_long : uzun ema değeri
    """
    def __init__(self,symbol,no_of_decimals,volume,parite,ema_short,ema_long):
        self.symbol = symbol
        self.no_of_decimals = no_of_decimals
        self.volume = volume
        self.parite = parite
        self.ema_short = ema_short
        self.ema_long = ema_long


    # Belirtilen sembol, miktar ve fiyatla sınırlı satış emri oluşturuyoruz
    def sell_market(self, symbol, quantity):
        output = client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity,
        )
        print(output)

    def buy_market(self, symbol, quantity):
        output = client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.FUTURE_ORDER_TYPE_MARKET,
            quantity=quantity,
        )
        print(output)


    # Belirtilen semboldeki pozisyonu kontrol et ve "LONG", "SHORT" veya "FLAT" olarak döndürür.
    def get_direction(self,symbol):
        x = client.futures_position_information(symbol=symbol)
        df = pd.DataFrame(x)
        if float(df["positionAmt"].sum()) > 0:
            return "LONG"
        if float(df["positionAmt"].sum()) < 0:
            return "SHORT"
        else:
            return "FLAT"

    def intersection_tracking(self, symbol, parite, ema_short, ema_long):
        interval = str(parite) + "m"

        # Belirli bir zaman aralığındaki klines verilerini almak için limit parametresini ekleyin
        klines = client.get_klines(symbol=symbol, interval=interval, limit=ema_long)

        # Verileri bir DataFrame'e dönüştürün
        df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time',
                                           'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
                                           'taker_buy_quote_asset_volume', 'ignore'])

        # Zaman sütununu datetime'a çevirin
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        # EMA'ları hesaplayın
        df['ema_short'] = df['close'].ewm(span=ema_short, adjust=False).mean()
        df['ema_long'] = df['close'].ewm(span=ema_long, adjust=False).mean()

        # Alım emri verme koşulunu kontrol edin
        if df['ema_short'].iloc[-1] > df['ema_long'].iloc[-1] and df['ema_short'].iloc[-2] <= df['ema_long'].iloc[-2]:
            return "LONG"
        else:
            return "SHORT"


    def run(self):
        while True:
            direction = self.get_direction(self.symbol)

            if direction == "FLAT":
                # Eğer pozisyon yoksa, kesişim durumuna göre işlem aç
                intersection_signal = self.intersection_tracking(self.symbol, self.parite, self.ema_short, self.ema_long)

                if intersection_signal == "LONG":
                    # EMA50, EMA200 yukarı keserse, long pozisyon aç
                    self.buy_market(self.symbol, self.volume)
                    print(f"Long pozisyon açıldı: {self.symbol}")

                elif intersection_signal == "SHORT":
                    # EMA50, EMA200 aşağı keserse, short pozisyon aç
                    self.sell_market(self.symbol, self.volume)
                    print(f"Short pozisyon açıldı: {self.symbol}")

            elif direction == "LONG":
                # Eğer pozisyon long ise ve EMA50, EMA200 aşağı keserse, long pozisyonu kapat
                intersection_signal = self.intersection_tracking(self.symbol, self.parite, self.ema_short, self.ema_long)

                if intersection_signal == "SHORT":
                    self.sell_market(self.symbol, self.volume)
                    print(f"Long pozisyon kapatıldı, short pozisyon açıldı: {self.symbol}")

            elif direction == "SHORT":
                # Eğer pozisyon short ise ve EMA50, EMA200 yukarı keserse, short pozisyonu kapat
                intersection_signal = self.intersection_tracking(self.symbol, self.parite, self.ema_short, self.ema_long)

                if intersection_signal == "LONG":
                    self.buy_market(self.symbol, self.volume)
                    print(f"Short pozisyon kapatıldı, long pozisyon açıldı: {self.symbol}")
