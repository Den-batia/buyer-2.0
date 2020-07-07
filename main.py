from __future__ import unicode_literals
import requests
import requests.auth
from datetime import datetime
import time
import api
from config import *
from API_keys import *

url = buy_list + '.json'
Me_1 = BuyURL
Me_id_1 = Me_1.split('/')[-2]
Me_3_1 = str("/api/ad-equation/" + Me_id_1 + "/")
url2 = 'https://httpbin.org/ip'


def loadqiwi(session, nam=None):
    
    ''' API запрос'''
    
    global t, a
    if nam is None:
        t = session.get(url).json()['data']['ad_list']
    else:
        session.proxies = {'https': proxy_logpas + nam}
        t = session.get(url).json()['data']['ad_list']
    return t


def info(req, High=None):
    
    '''Определение max цены'''
    
    lst = []
    for trader in range(len(req)):
        visible = req[trader]['data']['visible']
        price = float(req[trader]['data']['temp_price'])
        username = req[trader]['data']['profile']['username']
        if visible is False or price > High or any(word in username for word in list_ignore):
            pass
        else:
            lst.append(price)
    params = {u'price_equation': str(round(float(max(lst) + X), 2))}
    return params



def torg_loc(params, nam=None):
    
    '''API изменения цены'''
    
    if nam is None:
        nowtime = datetime.now().strftime('%H:%M:%S.%f')
        a = api.hmac(hmac_key, hmac_secret).call('POST', Me_3_1, params).json()
        print("-------------------------------------------------------", )
        print(str(a) + nowtime + "  Новая цена  : " + str(params.get('price_equation')) + '\t')
    else:
        nowtime = datetime.now().strftime('%H:%M:%S.%f')
        a = api.hmac(hmac_key, hmac_secret, proxy = {'https': proxy_logpas + nam}).call('POST', Me_3_1, params).json()
        print("-------------------------------------------------------", )
        print(str(a) + nowtime + "  Новая цена  : " + str(params.get('price_equation')) + '\t' + nam)



def bay():

    '''Отправка первого сообщения'''
    
    conn = api.hmac(hmac_key, hmac_secret)
    n = None
    while True:
        try:
            n = conn.call('GET', '/api/notifications/').json()['data']
        except Exception as e:
            print(e)

        for i, e in reversed(list(enumerate(n))):

            if e['read'] == False:
                s = e['msg']  # тело сообщения
                d = str(e['id'])  # id сообщения
                d1 = str('/api/notifications/mark_as_read/' + d + '/')  # api ключ
                k = str(e['contact_id'])  # id сделки
                k1 = str('/api/contact_message_post/' + k + '/')

                if 'Вы получили новое предложение' in s:
                    print('есть сообщение!')
                    print('начинаем процесс отправки реквезитов!!!')
                    conn.call('POST', k1, Msg1.encode('utf-8')).json()
                    conn.call('POST', d1).json()
                    print('\t реквезиты отправлены.\n')
                    continue
        time.sleep(10)



def main():
    requests_proxi = []
    api_proxy = []
    index_proxy = 0

    ''' Список проксей'''
    
    with open('12.txt') as f:
        for index, line in enumerate(f):
            if index < 6:
                requests_proxi.append(line.replace('*******', '').strip())
            else:
                api_proxy.append(line.replace('********', '').strip())

    with requests.Session() as session:
        while True:
            
            try:
                
                ''' Tекущая цена BTC'''
                
                high = float(session.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()['bpi']['USD']['rate'].replace(',','').split('.')[0]) * kurs * 0.99
            except Exception as e:
                print(e)

            ''' Основной цекл скрипта'''
                
            for i in requests_proxi:
                try:
                    a = loadqiwi(session, nam=i)
                    torg_loc(info(a, High=high), nam=api_proxy[index_proxy])
                except Exception as e:
                    print(e)
                    
                index_proxy +=1
                if index_proxy > len(api_proxy) - 1:
                    index_proxy = 0


if __name__ == '__main__':
    main()
