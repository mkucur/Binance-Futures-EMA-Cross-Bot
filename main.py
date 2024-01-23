
from classes import Bot
from threading import Thread

bot1 = Bot("BTCUSDT",1,0.2,1,50,200)
bot2 = Bot("ETHUSDT",2,0.2,1,50,200)

def b1():
    bot1.run()
def b2():
    bot2.run()

t1 = Thread(target=b1)
t2 = Thread(target=b2)

t1.start()
t2.start()



