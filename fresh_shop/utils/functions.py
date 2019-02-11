import random
import time
#生成订单交易号
def get_order_sn():
    s = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZZXCVBNM'
    order_sn = ''
    for i in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    return order_sn