import requests
from stock import get_stock
import time

key = 'xxxxxxxxxxxxxxxxxxxxx'  # your IFTTT web hook key
event_name = 'xxxxxxx'    # your IFTTT event name


def send_ifttt(v1):
    url = ('https://maker.ifttt.com/trigger/' + event_name + '/with/key/' + key +
           '?value1=' + str(v1))
    r = requests.get(url)  # send HTTP GET ,and get response
    if r.text[:5] == "Congr":
        print('already send (' + str(v1) + ') to Line')
    else:
        print("fail")
    return r.text


if __name__ == "__main__":
    msg = "資工2B<br>許世楨<br>406410026<br><br>\n"  # line ifttt msg <br> = \n

    stock_codes = ['3008', '2330', '2317']
    for code in stock_codes:
        print('get')
        msg += get_stock(code) + '<br>'
        time.sleep(5)

    ret = send_ifttt(msg)  # send HTTP request to IFTTT
    print('IFTTT response：', ret)

